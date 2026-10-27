"""Offline integration tests use generated WAV fixtures, never pretend to be platform results."""
import importlib.util
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import io
import json
import math
from pathlib import Path
import pickle
import struct
import subprocess
import sys
import tempfile
import threading
import unittest
import wave

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("music_skill", ROOT / "scripts/music.py")
skill = importlib.util.module_from_spec(spec)
spec.loader.exec_module(skill)


class MusicIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        audio = io.BytesIO()
        with wave.open(audio, "wb") as output:
            output.setnchannels(1)
            output.setsampwidth(2)
            output.setframerate(8000)
            output.writeframes(b"".join(struct.pack("<h", int(3000 * math.sin(2 * math.pi * 440 * i / 8000))) for i in range(8000)))
        cls.audio = audio.getvalue()

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                if self.path != "/fixture.wav":
                    self.send_error(404)
                    return
                self.send_response(200)
                self.send_header("Content-Type", "audio/wav")
                self.send_header("Content-Length", str(len(cls.audio)))
                self.end_headers()
                self.wfile.write(cls.audio)

            def log_message(self, *args):
                return  # Keep fixture-server request noise out of unittest output.

        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.state = self.root / "state"
        self.config = self.root / "config.json"
        self.config.write_text(json.dumps({"platforms": {"5sing": {"client": {"max_retries": 1}, "requests": {"timeout": [2, 3]}}}}))

    def cli(self, *args):
        completed = subprocess.run([sys.executable, str(ROOT / "scripts/music.py"), "--state-dir", str(self.state),
                                    "--config", str(self.config), *args], cwd=self.root, capture_output=True, text=True, timeout=40)
        return completed.returncode, json.loads(completed.stdout)

    def test_catalog_matches_registered_implementations_and_aliases(self):
        from musicdl.modules import MusicClientBuilder
        code, response = self.cli("sources")
        self.assertEqual(code, 0)
        self.assertEqual(response["count"], 17)
        for source in response["platforms"]:
            self.assertIn(source["client"], MusicClientBuilder.REGISTERED_MODULES)
        self.assertEqual(skill.platform_ids("网易云,QQ音乐,netease"), ["netease", "qq"])
        self.assertFalse(self.state.exists())

    def test_native_audio_objects_survive_private_snapshot(self):
        from musicdl.modules.utils import SongInfo
        from musicdl.modules.utils.appleutils import DownloadItem
        from musicdl.modules.utils.tidalutils import StreamUrl
        songs = [SongInfo(download_url=DownloadItem(media_metadata={"id": "fixture"})),
                 SongInfo(download_url=StreamUrl()), SongInfo(downloaded_contents=b"test fixture bytes")]
        snapshot = self.root / "native.pickle"
        with snapshot.open("wb") as handle:
            pickle.dump(songs, handle)
        with snapshot.open("rb") as handle:
            restored = pickle.load(handle)
        self.assertIsInstance(restored[0].download_url, DownloadItem)
        self.assertEqual(restored[0].download_url.media_metadata, {"id": "fixture"})
        self.assertIsInstance(restored[1].download_url, StreamUrl)
        self.assertEqual(restored[2].downloaded_contents, b"test fixture bytes")

    def test_real_http_batch_download_reports_partial_and_preserves_audio(self):
        from musicdl.modules.utils import SongInfo
        self.state.mkdir(mode=0o700)
        snapshot = self.state / "fixtures.pickle"
        base = f"http://127.0.0.1:{self.server.server_port}"
        songs = [SongInfo(source="FiveSingMusicClient", identifier=key, song_name="Generated test fixture", singers="Local fixture", ext="wav",
                          download_url=base + path, download_url_status={"ok": True}, duration_s=1)
                 for key, path in [("fixture", "/fixture.wav"), ("missing", "/missing.wav")]]
        with snapshot.open("wb") as handle:
            pickle.dump(songs, handle)
        with skill.database(self.state) as db:
            for position in range(2):
                db.execute("INSERT INTO candidates VALUES (?,?,?,?,?,?)", ("fixture-search", f"5sing:{position+1}", "5sing", str(snapshot), position, "{}"))
        code, response = self.cli("download", "--search-id", "fixture-search", "--items", "5sing:1,5sing:2", "--output", str(self.root / "downloads"), "--timeout", "30")
        self.assertEqual(code, 1, response)
        self.assertEqual(response["status"], "partial", response)
        self.assertEqual(response["downloaded"], 1, response)
        items = response["results"][0]["items"]
        self.assertEqual(items[0]["status"], "downloaded", response)
        self.assertEqual(items[1]["status"], "failed", response)
        with wave.open(items[0]["path"], "rb") as downloaded, wave.open(io.BytesIO(self.audio), "rb") as original:
            self.assertEqual(downloaded.readframes(8000), original.readframes(8000))
        self.assertNotIn("download_url", json.dumps(response))

    def test_unknown_candidate_is_explicit_failure(self):
        code, response = self.cli("download", "--search-id", "does-not-exist", "--items", "qq:1", "--output", str(self.root / "downloads"))
        self.assertEqual(code, 1)
        self.assertEqual(response["error_type"], "LookupError")
        self.assertFalse((self.root / "downloads").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
