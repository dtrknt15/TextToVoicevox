# -*- coding: utf-8 -*-
"""Mac 用 setup.command / 起動.command の Python の選び方を、偽の python で確かめる。

2026-10-03 の配布後チェックで見つかった2つの穴の再発防止:
  - 「ある」だけで python3 を選んでいたので、tkinter の無い Homebrew 版を選ぶと
    アプリが何も言わずに起動しなかった
  - venv_mac を --clear せずに作っていたので、作り直しが効かなかった

本物の Python や pip は使わず、呼ばれ方を記録するだけの偽 python（bash）を置く。
候補は setup.command のテスト用の T2V_PY_CANDIDATES で差し替える。bash があれば
Linux の CI でも動く（Windows は .command を使わないので飛ばす）。
"""
import os
import shutil
import subprocess
import time

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

pytestmark = pytest.mark.skipif(
    os.name == "nt" or shutil.which("bash") is None,
    reason="Mac 用のシェルスクリプトは bash のある Mac / Linux で確かめる")

# kind=good … tkinter の確かめ（-c に tkinter を含む）が通る Python
# kind=bad  … 動きはするが tkinter が無い Python（Homebrew の python-tk 無しなど）
# -m venv で作る venv の python は、元の Python の性質を引き継ぐ（自分をコピーする）
FAKE_PY = """#!/bin/bash
echo "$0 $*" >> "$T2V_TEST_LOG"
kind={kind}
if [ "$1" = -c ]; then
    case "$2" in *tkinter*) [ "$kind" = good ] && exit 0; exit 1 ;; esac
    exit 0
fi
if [ "$1" = -m ] && [ "$2" = venv ]; then
    for d; do :; done
    [ "$3" = --clear ] && rm -rf "$d"
    mkdir -p "$d/bin" && cp "$0" "$d/bin/python" && chmod +x "$d/bin/python"
    exit 0
fi
exit 0
"""


def _fake_python(path, kind):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(FAKE_PY.format(kind=kind))
    os.chmod(path, 0o755)
    return path


@pytest.fixture
def app(tmp_path):
    """配布 zip を展開したのと同じ並びの作業フォルダ（スクリプト＋requirements.txt）。"""
    d = tmp_path / "app"
    d.mkdir()
    for name in ("setup.command", "起動.command"):
        shutil.copy(os.path.join(ROOT, name), d / name)
    (d / "requirements.txt").write_text("", encoding="utf-8")
    (d / "main.py").write_text("", encoding="utf-8")
    pys = tmp_path / "pys"
    return {
        "dir": d,
        "log": tmp_path / "calls.log",
        "good": _fake_python(str(pys / "good" / "python3"), "good"),
        "bad": _fake_python(str(pys / "bad" / "python3"), "bad"),
    }


def _run(app, script, candidates):
    env = dict(os.environ, T2V_PY_CANDIDATES=":".join(candidates),
               T2V_TEST_LOG=str(app["log"]), LANG="ja_JP.UTF-8")
    r = subprocess.run(["bash", str(app["dir"] / script)], cwd=str(app["dir"]),
                       stdin=subprocess.DEVNULL, capture_output=True, env=env, timeout=60)
    return r.returncode, r.stdout.decode("utf-8", "replace") + r.stderr.decode("utf-8", "replace")


def _log(app):
    try:
        return app["log"].read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def _wait_for_main(app, timeout=5.0):
    """起動.command は main.py を nohup で裏に回すので、記録に出るまで少し待つ。"""
    end = time.time() + timeout
    while time.time() < end:
        if " main.py" in _log(app):
            return True
        time.sleep(0.1)
    return False


def test_setup_skips_python_without_tkinter(app):
    """tkinter の無い Python は飛ばし、次の候補（tkinter あり）で venv を --clear で作る。"""
    rc, out = _run(app, "setup.command", [app["bad"], "/nonexistent/python3", app["good"]])
    assert rc == 0, out
    assert "見送ります" in out and app["bad"] in out, out
    assert f"使用する Python: {app['good']}" in out, out
    log = _log(app)
    assert f"{app['good']} -m venv --clear venv_mac" in log, log
    assert f"{app['bad']} -m venv" not in log, log
    assert "venv_mac/bin/python -m pip install -r requirements.txt" in log, log


def test_setup_stops_with_guidance_when_no_tk_python(app):
    """使える Python が無ければ、venv を作らずに python.org / python-tk を案内して止まる。"""
    rc, out = _run(app, "setup.command", [app["bad"], "/nonexistent/python3"])
    assert rc == 1, out
    assert "https://www.python.org/downloads/" in out, out
    assert "brew install python-tk" in out, out
    assert "-m venv" not in _log(app)
    assert not (app["dir"] / "venv_mac").exists()


def test_setup_rebuilds_existing_venv(app):
    """前に作った venv_mac が残っていても、--clear で作り直す（作り直しが効く）。"""
    _fake_python(str(app["dir"] / "venv_mac" / "bin" / "python"), "bad")
    rc, out = _run(app, "setup.command", [app["good"]])
    assert rc == 0, out
    assert f"{app['good']} -m venv --clear venv_mac" in _log(app)


def test_setup_ignores_python_inside_venv_mac(app):
    """venv_mac の中の Python は、作り直す当の物なので候補から外す。"""
    inner = _fake_python(str(app["dir"] / "venv_mac" / "bin" / "python"), "good")
    rc, out = _run(app, "setup.command", [inner, app["good"]])
    assert rc == 0, out
    assert f"使用する Python: {app['good']}" in out, out


def test_launcher_rebuilds_venv_without_tkinter(app):
    """venv_mac の Python で tkinter が読めなければ、無言で終わらずに案内して作り直し、起動する。"""
    _fake_python(str(app["dir"] / "venv_mac" / "bin" / "python"), "bad")
    rc, out = _run(app, "起動.command", [app["good"]])
    assert rc == 0, out
    assert "tkinter" in out and "作り直します" in out, out
    assert f"{app['good']} -m venv --clear venv_mac" in _log(app)
    assert _wait_for_main(app), _log(app)


def test_launcher_stops_with_guidance_when_setup_fails(app):
    """作り直しても tkinter が使えなければ、main.py を起動せず、何を入れればよいか案内する。"""
    _fake_python(str(app["dir"] / "venv_mac" / "bin" / "python"), "bad")
    rc, out = _run(app, "起動.command", [app["bad"]])
    assert rc == 1, out
    assert "起動できませんでした" in out, out
    assert "brew install python-tk" in out and "setup.command" in out, out
    time.sleep(0.5)
    assert " main.py" not in _log(app)


def test_launcher_starts_directly_when_venv_is_fine(app):
    """venv_mac が健全なら、セットアップを挟まずにそのまま起動する。"""
    _fake_python(str(app["dir"] / "venv_mac" / "bin" / "python"), "good")
    rc, out = _run(app, "起動.command", [app["bad"]])
    assert rc == 0, out
    assert "-m venv" not in _log(app)
    assert _wait_for_main(app), _log(app)
