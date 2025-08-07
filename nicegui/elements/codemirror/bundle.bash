#!/bin/bash
set -e

cd "$(dirname "$0")"

echo "Installing dependencies..."
npm install

echo "Cleaning build directory..."
npm run clean

echo "Building CodeMirror bundle..."
npm run build

echo "Installed CodeMirror version:"
npm list codemirror --depth=0
