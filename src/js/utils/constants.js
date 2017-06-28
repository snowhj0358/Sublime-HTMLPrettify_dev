/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

import { parseJSON5 } from './jsonUtils';

export const DIAGNOSTICS_MARKER_BEGIN = '### HTMLPrettify diagnostics begin ###';
export const DIAGNOSTICS_MARKER_END = '### HTMLPrettify diagnostics end ###';
export const PRETTIFIED_CODE_MARKER_BEGIN = '### HTMLPrettify prettified code begin ###';
export const PRETTIFIED_CODE_MARKER_END = '### HTMLPrettify prettified code end ###';

// The source file to be prettified, original source's path and some options.
export const EDITOR_FILE_SYNTAX = process.argv[2];
export const EDITOR_INDENT_SIZE = process.argv[3];
export const EDITOR_INDENT_WITH_TABS = process.argv[4];
export const RESPECT_EDITORCONFIG_FILES = process.argv[5];
export const GLOBAL_FILE_RULES = parseJSON5(process.argv[6]);
export const EDITOR_TEXT_FILE_PATH = process.argv[7];
export const ORIGINAL_FILE_PATH = process.argv[8];
export const CONFIG_EXTRA_LOOKUP_PATHS = [process.argv[9], process.argv[10]];
