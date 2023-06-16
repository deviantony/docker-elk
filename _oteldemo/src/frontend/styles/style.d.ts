// Copyright The OpenTelemetry Authors
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

import 'styled-components';

declare module 'styled-components' {
  export interface DefaultTheme {
    colors: {
      otelBlue: string;
      otelYellow: string;
      otelGray: string;
      otelRed: string;
      backgroundGray: string;
      lightBorderGray: string;
      borderGray: string;
      textGray: string; 
      textLightGray: string;
      white: string;
    };
    sizes: {
      mLarge: string;
      mxLarge: string;
      mMedium: string;
      mSmall: string;
      dLarge: string;
      dxLarge: string;
      dMedium: string;
      dSmall: string;
      nano: string;
    };
    breakpoints: {
      desktop: string;
    };
    fonts: {
      bold: string;
      regular: string;
      semiBold: string;
      light: string;
    };
  }
}
