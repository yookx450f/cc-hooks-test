#!/bin/bash
cd "$(dirname "$0")"
if uvx pytest -q > /dev/null 2>&1; then
  exit 0
else
  echo "テストが失敗しています。pytest の失敗内容を確認して修正してください。" >&2
  exit 2
fi