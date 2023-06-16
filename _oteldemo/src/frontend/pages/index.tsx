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

import { NextPage } from 'next';
import Footer from '../components/Footer';
import Layout from '../components/Layout';
import ProductList from '../components/ProductList';
import * as S from '../styles/Home.styled';
import { useQuery } from 'react-query';
import ApiGateway from '../gateways/Api.gateway';
import Banner from '../components/Banner';
import { CypressFields } from '../utils/Cypress';
import { useCurrency } from '../providers/Currency.provider';

const Home: NextPage = () => {
  const { selectedCurrency } = useCurrency();
  const { data: productList = [] } = useQuery(['products', selectedCurrency], () =>
    ApiGateway.listProducts(selectedCurrency)
  );

  return (
    <Layout>
      <S.Home data-cy={CypressFields.HomePage}>
        <Banner />
        <S.Container>
          <S.Row>
            <S.Content>
              <S.HotProducts>
                <S.HotProductsTitle data-cy={CypressFields.HotProducts} id="hot-products">
                  Hot Products
                </S.HotProductsTitle>
                <ProductList productList={productList} />
              </S.HotProducts>
            </S.Content>
          </S.Row>
        </S.Container>
        <Footer />
      </S.Home>
    </Layout>
  );
};

export default Home;
