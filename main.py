import os
import sys
from pathlib import Path

from app.core.runtime import prepare_windowed_runtime, stdio_self_test

# Must run before PySide6 / Hugging Face / OpenVINO imports in a windowed EXE.
prepare_windowed_runtime()


def self_test(argv):
    from app.core.diagnostics import environment_report
    out = argv[0] if argv else str(Path.cwd() / 'JunbaAITranscriber_SELFTEST.txt')
    ok, report = environment_report(str(Path(out).parent), '')
    Path(out).write_text(('SELFTEST_OK\n' if ok else 'SELFTEST_FAILED\n') + report, encoding='utf-8')
    return 0 if ok else 2


def ui_self_test(argv):
    os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
    out = argv[0] if argv else str(Path.cwd() / 'JunbaAITranscriber_UI_SELFTEST.txt')
    try:
        from PySide6.QtWidgets import QApplication
        from app.ui.main_window import MainWindow
        app = QApplication.instance() or QApplication([])
        win = MainWindow()
        checks = []
        checks.append(('version', 'v3.1' in win.windowTitle()))
        checks.append(('traditional-label', '繁體中文' in win.language.itemText(1)))
        checks.append(('traditional-default', win.traditional.isChecked()))
        checks.append(('stop-exports-partial-label', '停止並輸出目前結果' in win.stop_btn.text()))
        checks.append(('hardware-adaptive-option', win.accel.findData('adaptive') >= 0))
        checks.append(('hardware-performance-option', win.accel.findData('performance') >= 0))
        checks.append(('hardware-eco-option', win.accel.findData('eco') >= 0))
        checks.append(('auto-model-option', win.model.findData('auto') >= 0))
        checks.append(('traditional-author', '峻爸' in win.windowTitle()))
        checks.append(('hardware-npu-option', win.accel.findData('openvino_npu') >= 0))
        checks.append(('hardware-intel-gpu-option', win.accel.findData('openvino_gpu') >= 0))
        checks.append(('hardware-cuda-option', win.accel.findData('cuda') >= 0))
        checks.append(('hardware-cpu-option', win.accel.findData('cpu') >= 0))
        checks.append(('large-v3-turbo-option', win.model.findText('large-v3-turbo') >= 0))
        checks.append(('activity-monitor-state', hasattr(win, 'activity_state')))
        checks.append(('activity-monitor-time', hasattr(win, 'activity_time')))
        checks.append(('activity-timer-active', win.activity_timer.isActive()))
        win.mode.setCurrentText('Google Gemini')
        app.processEvents()
        checks.append(('google-diar-enabled', win.diar.isEnabled()))
        checks.append(('google-timestamps-enabled', win.timestamps.isEnabled()))
        win.smart.setChecked(True)
        app.processEvents()
        checks.append(('smart-auto-disables-diar', not win.diar.isChecked()))
        checks.append(('smart-auto-disables-timestamps', not win.timestamps.isChecked()))
        win.smart.setChecked(False)
        win.diar.setChecked(True)
        win.timestamps.setChecked(True)
        app.processEvents()
        checks.append(('diar-and-timestamps-together', win.diar.isChecked() and win.timestamps.isChecked() and not win.smart.isChecked()))
        ok = all(v for _, v in checks)
        report = '\n'.join(f"{'PASS' if v else 'FAIL'} {k}" for k, v in checks)
        Path(out).write_text(('UI_SELFTEST_OK\n' if ok else 'UI_SELFTEST_FAILED\n') + report, encoding='utf-8')
        win.close()
        return 0 if ok else 3
    except Exception as e:
        Path(out).write_text(f'UI_SELFTEST_FAILED\n{type(e).__name__}: {e}\n', encoding='utf-8')
        return 3



def openvino_binary_self_test(argv):
    out = argv[0] if argv else str(Path.cwd() / 'OPENVINO_BINARY_SELFTEST.txt')
    try:
        from app.core.openvino_runtime import binary_self_test
        ok, report = binary_self_test()
    except Exception as e:
        ok, report = False, f'{type(e).__name__}: {e}'
    Path(out).write_text(('OPENVINO_BINARY_SELFTEST_OK\n' if ok else 'OPENVINO_BINARY_SELFTEST_FAILED\n') + report, encoding='utf-8')
    return 0 if ok else 5

def main():
    if '--windowed-io-self-test' in sys.argv:
        i = sys.argv.index('--windowed-io-self-test')
        out = sys.argv[i+1] if i+1 < len(sys.argv) else str(Path.cwd()/'WINDOWED_IO_SELFTEST.txt')
        raise SystemExit(stdio_self_test(out))
    if '--openvino-binary-self-test' in sys.argv:
        i = sys.argv.index('--openvino-binary-self-test')
        raise SystemExit(openvino_binary_self_test(sys.argv[i+1:i+2]))
    if '--self-test' in sys.argv:
        i = sys.argv.index('--self-test')
        raise SystemExit(self_test(sys.argv[i+1:i+2]))
    if '--ui-self-test' in sys.argv:
        i = sys.argv.index('--ui-self-test')
        raise SystemExit(ui_self_test(sys.argv[i+1:i+2]))
    from PySide6.QtWidgets import QApplication
    from app.ui.main_window import MainWindow
    app = QApplication(sys.argv)
    app.setApplicationName('峻爸 AI Transcriber')
    app.setOrganizationName('Junba')
    win = MainWindow(); win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
