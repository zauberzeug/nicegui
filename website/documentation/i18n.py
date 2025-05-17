# ruff: noqa: RUF001

import re

from nicegui import app

mydict = {
    'id1': {
        'en': 'Overview',
        'cn': '概述',
        'jp': '概要',
        'de': 'Überblick',
    },

    'id2': {
        'en': '''NiceGUI is an open-source Python library to write graphical user interfaces which run in the browser.
    It has a very gentle learning curve while still offering the option for advanced customizations.
    NiceGUI follows a backend-first philosophy:
    It handles all the web development details.
    You can focus on writing Python code.
    This makes it ideal for a wide range of projects including short
    scripts, dashboards, robotics projects, IoT solutions, smart home automation, and machine learning.''',
        'cn': '''NiceGUI 是一个开源的 Python 库，用于编写在浏览器中运行的图形用户界面。
    它具有非常温和的学习曲线，同时仍然提供高级自定义的选项。
    NiceGUI 遵循后端优先的理念：
    它处理所有 Web 开发的细节。
    您可以专注于编写 Python 代码。
    这使它非常适合广泛的项目，包括短脚本、仪表板、机器人项目、物联网解决方案、智能家居自动化和机器学习。''',
        'jp': '''NiceGUIは、ブラウザで実行されるグラフィカルユーザーインターフェイスを作成するためのオープンソースのPythonライブラリです。
    非常に緩やかな学習曲線を持ちながら、高度なカスタマイズのオプションも提供しています。
    NiceGUIはバックエンドファーストの哲学に従っています。
    すべてのWeb開発の詳細を処理します。
    Pythonコードの記述に集中できます。
    これにより、短いスクリプト、ダッシュボード、ロボティクスプロジェクト、IoTソリューション、スマートホームオートメーション、機械学習など、幅広いプロジェクトに最適です。''',
        'de': '''NiceGUI ist eine Open-Source-Python-Bibliothek zur Erstellung grafischer Benutzeroberflächen, die im Browser ausgeführt werden.
    Sie hat eine sehr sanfte Lernkurve und bietet dennoch die Möglichkeit zu erweiterten Anpassungen.
    NiceGUI folgt einer Backend-First-Philosophie:
    Es kümmert sich um alle Details der Webentwicklung.
    Sie können sich auf das Schreiben von Python-Code konzentrieren.
    Dies macht es ideal für eine Vielzahl von Projekten, darunter kurze
    Skripte, Dashboards, Robotikprojekte, IoT-Lösungen, Smart-Home-Automatisierung und maschinelles Lernen.''',
    },
}


def i18nify(text: str):
    try:
        language = app.storage.user['language']
    except Exception as e:
        print('Error getting language:', e)
        language = 'en'
    return i18nify_language(text, language=language)


def i18nify_language(text: str, *, language: str = 'en') -> str:
    """Translate the given text to the specified language."""

    # Look for the HTML tag <!--TRANSLATEID-{uuid}--> in the text using regex
    print('i18nify_language', text, language)
    match = re.search(r'<!--TRANSLATEID-([a-zA-Z0-9-]+)-->', text)
    if not match:
        return drop_the_tag(text)

    translation_id = match.group(1)
    if not translation_id or translation_id not in mydict or language not in mydict[translation_id]:
        return drop_the_tag(text)

    text = mydict[translation_id].get(language, mydict[translation_id][language])
    return text


def drop_the_tag(text: str) -> str:
    """Remove the HTML tag from the text."""
    # Remove the HTML tag <!--TRANSLATEID-{uuid}--> from the text
    return re.sub(r'<!--TRANSLATEID-[a-zA-Z0-9-]+-->', '', text)
