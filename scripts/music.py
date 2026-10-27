#!/usr/bin/env python3
"""Noninteractive musicdl adapter. Public stdout contains JSON only."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from contextlib import redirect_stderr, redirect_stdout
from functools import wraps
import importlib.metadata
import json
import os
from pathlib import Path
import pickle
import sqlite3
import subprocess
import sys
import time
import traceback
import uuid

# This catalog deliberately matches the 17 choices in the original GUI.
PLATFORMS = {
    "apple": ("苹果音乐", "AppleMusicClient", ["applemusic", "Apple Music"]),
    "deezer": ("Deezer", "DeezerMusicClient", []),
    "5sing": ("5sing", "FiveSingMusicClient", ["fivesing"]),
    "jamendo": ("Jamendo", "JamendoMusicClient", []),
    "joox": ("Joox", "JooxMusicClient", []),
    "kuwo": ("酷我音乐", "KuwoMusicClient", ["酷我", "kw"]),
    "kugou": ("酷狗音乐", "KugouMusicClient", ["酷狗", "kg"]),
    "migu": ("咪咕音乐", "MiguMusicClient", ["咪咕"]),
    "netease": ("网易云音乐", "NeteaseMusicClient", ["网易云", "网易", "wyy"]),
    "qq": ("QQ音乐", "QQMusicClient", ["qqmusic", "QQ 音乐"]),
    "qianqian": ("千千音乐", "QianqianMusicClient", ["千千"]),
    "qobuz": ("Qobuz", "QobuzMusicClient", []),
    "soundcloud": ("SoundCloud", "SoundCloudMusicClient", ["sc"]),
    "streetvoice": ("StreetVoice", "StreetVoiceMusicClient", ["街声", "街聲"]),
    "soda": ("汽水音乐", "SodaMusicClient", ["汽水"]),
    "spotify": ("Spotify", "SpotifyMusicClient", []),
    "tidal": ("TIDAL", "TIDALMusicClient", []),
}
DEFAULT_TIMEOUT = 120.0  # Per-platform operation deadline, configurable with --timeout.
DEFAULT_JOBS = 3         # Number of concurrent platform operations, configurable with --jobs.
DEFAULT_LIMIT = 5        # Search results requested per platform, configurable with --limit.


def platform_ids(value):
    aliases = {}
    for key, (name, client, other) in PLATFORMS.items():
        for alias in [key, name, client, *other]:
            aliases[alias.casefold()] = key
    result = []
    for name in value.split(","):
        try:
            key = aliases[name.strip().casefold()]
        except KeyError:
            raise argparse.ArgumentTypeError(f"Unknown platform: {name}; use sources") from None
        if key not in result:
            result.append(key)
    return result


def json_write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def database(state):
    state.mkdir(parents=True, exist_ok=True, mode=0o700)
    db = sqlite3.connect(state / "catalog.sqlite3")
    db.execute("CREATE TABLE IF NOT EXISTS candidates (search_id TEXT, item_id TEXT, platform TEXT, snapshot TEXT, position INTEGER, summary TEXT, PRIMARY KEY(search_id,item_id))")
    return db


def load_config(path):
    if path is not None:
        return json.loads(Path(path).expanduser().read_text(encoding="utf-8"))
    default = Path.home() / ".config/music-download/config.json"
    return json.loads(default.read_text(encoding="utf-8")) if default.exists() else {}


class OperationLog:
    def __init__(self, handle):
        self.handle = handle
        self.errors = 0
        self.warnings = 0

    def __deepcopy__(self, memo):
        # musicdl clones constructor config; log handles remain shared within this worker.
        return self

    def info(self, message, **kwargs):
        print("INFO", message, file=self.handle, flush=True)

    def warning(self, message, **kwargs):
        self.warnings += 1
        print("WARNING", message, file=self.handle, flush=True)

    def error(self, message, **kwargs):
        self.errors += 1
        print("ERROR", message, file=self.handle, flush=True)

    def debug(self, message, **kwargs):
        print("DEBUG", message, file=self.handle, flush=True)


def record_resolvers(client):
    """Tag actual returned objects, preserving third-party provenance in official parsers."""
    for name in dir(client):
        if not name.startswith("_parsewith") or name == "_parsewiththirdpartapis":
            continue
        method = getattr(client, name)
        if not callable(method):
            continue

        def decorate(original, method_name):
            @wraps(original)
            def call(*args, **kwargs):
                song = original(*args, **kwargs)
                if song is not None and getattr(song, "with_valid_download_url", False):
                    if not hasattr(song, "_skill_resolver"):
                        song._skill_resolver = {
                            "kind": "platform_api" if method_name.startswith("_parsewithofficial") else "third_party",
                            "method": method_name,
                        }
                return song
            return call

        setattr(client, name, decorate(method, name))


def song_summary(song):
    return {
        "title": song.song_name, "artist": song.singers, "album": song.album,
        "platform_client": song.source, "identifier": song.identifier,
        "format": song.ext, "size": song.file_size,
        "size_bytes": song.file_size_bytes if isinstance(song.file_size_bytes, (int, float)) else None,
        "duration_seconds": song.duration_s,
        "resolver": getattr(song, "_skill_resolver", None),
    }


def worker(request_path):
    request = json.loads(Path(request_path).read_text(encoding="utf-8"))
    job = Path(request_path).parent
    result = {"platform": request["platform"], "items": []}
    with (job / "backend.log").open("w", encoding="utf-8") as handle, redirect_stdout(handle), redirect_stderr(handle):
        logger = OperationLog(handle)
        try:
            from musicdl.modules import BuildMusicClient
            label, client_name, aliases = PLATFORMS[request["platform"]]
            settings = request["settings"]
            cfg = dict(settings.get("client", {}))
            cfg.update(type=client_name, work_dir=str(job / "work"), logger_handle=logger, disable_print=True)
            if "limit" in request:
                cfg["search_size_per_source"] = request["limit"]
            client = BuildMusicClient(module_cfg=cfg)
            record_resolvers(client)
            overrides = dict(settings.get("requests", {}))
            # JSON arrays represent requests' (connect_timeout, read_timeout) tuple.
            if isinstance(overrides.get("timeout"), list):
                overrides["timeout"] = tuple(overrides["timeout"])
            threads = settings.get("threads", 1)
            action = request["action"]
            if action == "search":
                songs = client.search(keyword=request["query"], num_threadings=threads, request_overrides=overrides)
            elif action == "playlist":
                songs = client.parseplaylist(request["url"], request_overrides=overrides)
            elif action == "download":
                # Only load snapshots created in this installation's private state directory.
                with Path(request["snapshot"]).open("rb") as handle_in:
                    songs = pickle.load(handle_in)
                selected = []
                for item in request["selected"]:
                    song = songs[item["position"]]
                    song.work_dir = request["output"]
                    song._save_path = None
                    selected.append(song)
                downloaded = client.download(selected, num_threadings=threads, request_overrides=overrides)
                by_key = {(song.source, song.identifier): song for song in downloaded}
                for item, song in zip(request["selected"], selected):
                    returned = by_key.get((song.source, song.identifier))
                    summary = song_summary(song)
                    summary["item_id"] = item["item_id"]
                    if returned is None:
                        summary.update(status="failed", reason="backend_did_not_return_downloaded_song")
                    else:
                        path = Path(returned.save_path)
                        if path.is_file():
                            summary.update(status="downloaded", path=str(path.resolve()), downloaded_bytes=path.stat().st_size)
                        else:
                            summary.update(status="failed", reason="backend_returned_missing_file")
                    result["items"].append(summary)
                successes = sum(item["status"] == "downloaded" for item in result["items"])
                result["status"] = "ok" if successes == len(selected) else "partial" if successes else "failed"
            else:
                raise ValueError(f"Unknown action: {action}")
            if action in {"search", "playlist"}:
                # Pickle retains musicdl's typed Apple/TIDAL URLs, nested SongInfo and bytes.
                with (job / "songs.pickle").open("wb") as handle_out:
                    pickle.dump(songs, handle_out, protocol=pickle.HIGHEST_PROTOCOL)
                result["items"] = [song_summary(song) for song in songs]
                result["status"] = "ok" if songs else "failed" if logger.errors else "no_downloadable_results"
        except Exception as error:
            traceback.print_exc(file=handle)
            result.update(status="error", error_type=type(error).__name__, reason="backend_operation_failed; inspect private backend.log")
        result["diagnostics"] = {"errors": logger.errors, "warnings": logger.warnings}
    json_write(job / "result.json", result)


def execute_job(request, job, timeout):
    job.mkdir(parents=True, mode=0o700)
    json_write(job / "request.json", request)
    started = time.monotonic()
    with (job / "process.log").open("w", encoding="utf-8") as handle:
        try:
            completed = subprocess.run(
                [sys.executable, str(Path(__file__).resolve()), "_worker", str(job / "request.json")],
                cwd=job, stdout=handle, stderr=handle, timeout=timeout, check=False,
            )
        except subprocess.TimeoutExpired:
            return {"platform": request["platform"], "status": "timeout", "items": [], "timeout_seconds": timeout,
                    "elapsed_seconds": round(time.monotonic() - started, 2), "log_path": str(job / "backend.log")}
    if completed.returncode != 0:
        return {"platform": request["platform"], "status": "worker_failed", "items": [],
                "exit_code": completed.returncode, "log_path": str(job / "process.log")}
    result = json.loads((job / "result.json").read_text(encoding="utf-8"))
    result.update(elapsed_seconds=round(time.monotonic() - started, 2), log_path=str(job / "backend.log"))
    return result


def collect(args, config, state):
    search_id = uuid.uuid4().hex
    run_dir = state / "runs" / search_id
    requests = []
    for platform in args.sources:
        request = {"action": args.command, "platform": platform, "settings": config.get("platforms", {}).get(platform, {})}
        if args.command == "search":
            request.update(query=args.query, limit=args.limit)
        else:
            request["url"] = args.url
        requests.append(request)
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        results = list(pool.map(lambda request: execute_job(request, run_dir / request["platform"], args.timeout), requests))
    with database(state) as db:
        for result in results:
            platform = result["platform"]
            for position, summary in enumerate(result["items"]):
                item_id = f"{platform}:{position + 1}"
                summary["item_id"] = item_id
                db.execute("INSERT INTO candidates VALUES (?,?,?,?,?,?)", (
                    search_id, item_id, platform, str(run_dir / platform / "songs.pickle"), position,
                    json.dumps(summary, ensure_ascii=False),
                ))
    total = sum(len(result["items"]) for result in results)
    all_ok = all(result["status"] == "ok" for result in results)
    status = "ok" if all_ok else "partial" if total else "no_downloadable_results" if all(result["status"] == "no_downloadable_results" for result in results) else "failed"
    return {"status": status, "search_id": search_id, "action": args.command, "results": results, "count": total}


def download(args, config, state):
    groups = {}
    with database(state) as db:
        for item_id in dict.fromkeys(args.items.split(",")):
            row = db.execute("SELECT platform,snapshot,position FROM candidates WHERE search_id=? AND item_id=?", (args.search_id, item_id)).fetchone()
            if row is None:
                raise LookupError(f"Candidate not found: {args.search_id}/{item_id}")
            platform, snapshot, position = row
            group = groups.setdefault((platform, snapshot), [])
            group.append({"item_id": item_id, "position": position})
    output = Path(args.output).expanduser().resolve()
    output.mkdir(parents=True, exist_ok=True)
    run_dir = state / "downloads" / uuid.uuid4().hex
    requests = []
    for (platform, snapshot), selected in groups.items():
        requests.append({"action": "download", "platform": platform, "snapshot": snapshot, "selected": selected,
                         "output": str(output), "settings": config.get("platforms", {}).get(platform, {})})
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        results = list(pool.map(lambda request: execute_job(request, run_dir / request["platform"], args.timeout), requests))
    success = sum(item["status"] == "downloaded" for result in results for item in result["items"])
    total = sum(len(request["selected"]) for request in requests)
    return {"status": "ok" if success == total else "partial" if success else "failed", "downloaded": success,
            "requested": total, "output": str(output), "results": results}


def main():
    os.umask(0o077)
    if len(sys.argv) == 3 and sys.argv[1] == "_worker":
        worker(sys.argv[2])
        return 0
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state-dir", default=os.environ.get("MUSIC_DOWNLOAD_STATE_DIR", str(Path.home() / ".local/share/music-download")))
    parser.add_argument("--config", help="External JSON config; defaults to ~/.config/music-download/config.json if present")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("sources")
    for action in ["search", "playlist", "download"]:
        command = sub.add_parser(action)
        command.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT, help="Per-platform process deadline in seconds")
        command.add_argument("--jobs", type=int, default=DEFAULT_JOBS, help="Concurrent platform processes")
        if action == "search":
            command.add_argument("--query", required=True)
            command.add_argument("--limit", type=int, default=DEFAULT_LIMIT)
        if action in {"search", "playlist"}:
            command.add_argument("--sources", type=platform_ids, required=True, help="Comma-separated platform names; selected by agent or user")
        if action == "playlist":
            command.add_argument("--url", required=True)
        if action == "download":
            command.add_argument("--search-id", required=True)
            command.add_argument("--items", required=True, help="Comma-separated candidate IDs from search/playlist")
            command.add_argument("--output", required=True)
    args = parser.parse_args()
    try:
        config = load_config(args.config)
        if args.command == "sources":
            result = {"engine": "musicdl", "version": importlib.metadata.version("musicdl"), "count": len(PLATFORMS), "platforms": [
                {"id": key, "name": value[0], "client": value[1], "aliases": value[2],
                 "configured": key in config.get("platforms", {})} for key, value in PLATFORMS.items()
            ]}
        else:
            state = Path(args.state_dir).expanduser().resolve()
            state.mkdir(parents=True, exist_ok=True, mode=0o700)
            result = download(args, config, state) if args.command == "download" else collect(args, config, state)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result.get("status") in {None, "ok", "no_downloadable_results"} else 1
    except Exception as error:
        print(json.dumps({"status": "error", "error_type": type(error).__name__, "message": str(error)}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    sys.exit(main())
