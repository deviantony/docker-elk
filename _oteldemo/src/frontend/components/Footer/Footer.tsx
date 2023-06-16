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

import { useEffect, useState } from 'react';
import * as S from './Footer.styled';
import SessionGateway from '../../gateways/Session.gateway';
import { CypressFields } from '../../utils/Cypress';

const currentYear = new Date().getFullYear();

const { userId } = SessionGateway.getSession();

const Footer = () => {
  const [sessionId, setSessionId] = useState('');

  useEffect(() => {
    setSessionId(userId);
  }, []);

  return (
    <S.Footer>
      <div>
        <p>This website is hosted for demo purpose only. It is not an actual shop.</p>
        <p>
          <span data-cy={CypressFields.SessionId}>session-id: {sessionId}</span>
        </p>
      </div>
      <p>
        @ {currentYear} OpenTelemetry (<a href="https://github.com/open-telemetry/opentelemetry-demo">Source Code</a>)
      </p>
    </S.Footer>
  );
};

export default Footer;
