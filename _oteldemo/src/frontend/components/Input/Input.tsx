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

import { HTMLInputTypeAttribute, InputHTMLAttributes } from 'react';
import * as S from './Input.styled';

interface IProps extends InputHTMLAttributes<HTMLSelectElement | HTMLInputElement> {
  type: HTMLInputTypeAttribute | 'select';
  children?: React.ReactNode;
  label: string;
}

const Input = ({ type, id = '', children, label, ...props }: IProps) => {
  return (
    <S.InputRow>
      <S.InputLabel>{label}</S.InputLabel>
      {type === 'select' ? (
        <>
          <S.Select id={id} {...props}>
            {children}
          </S.Select>
          <S.Arrow />
        </>
      ) : (
        <S.Input id={id} {...props} type={type} />
      )}
    </S.InputRow>
  );
};

export default Input;
