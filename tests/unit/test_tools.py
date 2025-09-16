# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from unittest.mock import patch, MagicMock

from app.agent import list_baseline_images

def test_list_baseline_images_success():
    """Tests that the tool correctly lists PNG files from the directory."""
    mock_listdir = ["image1.png", "image2.jpg", "image3.png", "document.txt"]
    expected_files = [os.path.join("images_baseline", "image1.png"), os.path.join("images_baseline", "image3.png")]

    with patch("os.listdir", return_value=mock_listdir):
        # The tool_context argument is not used in the current implementation, so we can pass a mock.
        result = list_baseline_images(tool_context=MagicMock())
        assert result == expected_files

def test_list_baseline_images_file_not_found():
    """Tests that the tool handles a FileNotFoundError gracefully."""
    with patch("os.listdir", side_effect=FileNotFoundError):
        result = list_baseline_images(tool_context=MagicMock())
        assert result == ["Error: 'images_baseline' directory not found."]

def test_list_baseline_images_empty_directory():
    """Tests that the tool returns an empty list for an empty directory."""
    with patch("os.listdir", return_value=[]):
        result = list_baseline_images(tool_context=MagicMock())
        assert result == []
