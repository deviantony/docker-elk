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

import { CypressFields } from '../../utils/Cypress';
import { Product } from '../../protos/demo';
import ProductCard from '../ProductCard';
import * as S from './ProductList.styled';

interface IProps {
  productList: Product[];
}

const ProductList = ({ productList }: IProps) => {
  return (
    <S.ProductList data-cy={CypressFields.ProductList}>
      {productList.map(product => (
        <ProductCard key={product.id} product={product} />
      ))}
    </S.ProductList>
  );
};

export default ProductList;
