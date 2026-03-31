# Fixture format

Each fixture file should contain:

1. A title line with desktop index and desktop name.
2. A short metadata section with desktop id and window count.
3. A layout summary that explains whether the desktop is empty, stacked, fullscreen, floating, or mixed.
4. A visible content summary that records anything readable from screenshots or OCR.
5. One `### Window N` section per tracked KWin window.

Fallback order for content details:

1. Exact text visible in the screenshot
2. OCR output
3. AT-SPI `Name` / `Description` / role data
4. Window title and class
5. Honest statement that the content is not recoverable from the current metadata
