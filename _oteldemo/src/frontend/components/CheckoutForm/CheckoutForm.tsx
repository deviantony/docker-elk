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

import Link from 'next/link';
import { useCallback, useState } from 'react';
import { CypressFields } from '../../utils/Cypress';
import Input from '../Input';
import * as S from './CheckoutForm.styled';

const currentYear = new Date().getFullYear();
const yearList = Array.from(new Array(20), (v, i) => i + currentYear);

export interface IFormData {
  email: string;
  streetAddress: string;
  city: string;
  state: string;
  country: string;
  zipCode: string;
  creditCardNumber: string;
  creditCardCvv: number;
  creditCardExpirationYear: number;
  creditCardExpirationMonth: number;
}

interface IProps {
  onSubmit(formData: IFormData): void;
}

const CheckoutForm = ({ onSubmit }: IProps) => {
  const [
    {
      email,
      streetAddress,
      city,
      state,
      country,
      zipCode,
      creditCardCvv,
      creditCardExpirationMonth,
      creditCardExpirationYear,
      creditCardNumber,
    },
    setFormData,
  ] = useState<IFormData>({
    email: 'someone@example.com',
    streetAddress: '1600 Amphitheatre Parkway',
    city: 'Mountain View',
    state: 'CA',
    country: 'United States',
    zipCode: "94043",
    creditCardNumber: '4432-8015-6152-0454',
    creditCardCvv: 672,
    creditCardExpirationYear: 2030,
    creditCardExpirationMonth: 1,
  });

  const handleChange = useCallback((e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setFormData(formData => ({
      ...formData,
      [e.target.name]: e.target.value,
    }));
  }, []);

  return (
    <S.CheckoutForm
      onSubmit={event => {
        event.preventDefault();
        onSubmit({
          email,
          streetAddress,
          city,
          state,
          country,
          zipCode,
          creditCardCvv,
          creditCardExpirationMonth,
          creditCardExpirationYear,
          creditCardNumber,
        });
      }}
    >
      <S.Title>Shipping Address</S.Title>

      <Input
        label="E-mail Address"
        type="email"
        id="email"
        name="email"
        value={email}
        required
        onChange={handleChange}
      />
      <Input
        label="Street Address"
        type="text"
        name="streetAddress"
        id="street_address"
        value={streetAddress}
        onChange={handleChange}
        required
      />
      <Input
        label="Zip Code"
        type="text"
        name="zipCode"
        id="zip_code"
        value={zipCode}
        onChange={handleChange}
        required
      />
      <Input label="City" type="text" name="city" id="city" value={city} required onChange={handleChange} />

      <S.StateRow>
        <Input label="State" type="text" name="state" id="state" value={state} required onChange={handleChange} />
        <Input
          label="Country"
          type="text"
          id="country"
          placeholder="Country Name"
          name="country"
          value={country}
          onChange={handleChange}
          required
        />
      </S.StateRow>

      <div>
        <S.Title>Payment Method</S.Title>
      </div>

      <Input
        type="text"
        label="Credit Card Number"
        id="credit_card_number"
        name="creditCardNumber"
        placeholder="0000-0000-0000-0000"
        value={creditCardNumber}
        onChange={handleChange}
        required
        pattern="\d{4}-\d{4}-\d{4}-\d{4}"
      />

      <S.CardRow>
        <Input
          label="Month"
          name="creditCardExpirationMonth"
          id="credit_card_expiration_month"
          value={creditCardExpirationMonth}
          onChange={handleChange}
          type="select"
        >
          <option value="1">January</option>
          <option value="2">February</option>
          <option value="3">March</option>
          <option value="4">April</option>
          <option value="5">May</option>
          <option value="6">June</option>
          <option value="7">July</option>
          <option value="8">August</option>
          <option value="9">September</option>
          <option value="10">October</option>
          <option value="11">November</option>
          <option value="12">January</option>
        </Input>
        <Input
          label="Year"
          name="creditCardExpirationYear"
          id="credit_card_expiration_year"
          value={creditCardExpirationYear}
          onChange={handleChange}
          type="select"
        >
          {yearList.map(year => (
            <option value={year} key={year}>
              {year}
            </option>
          ))}
        </Input>
        <Input
          label="CVV"
          type="password"
          id="credit_card_cvv"
          name="creditCardCvv"
          value={creditCardCvv}
          required
          pattern="\d{3}"
          onChange={handleChange}
        />
      </S.CardRow>

      <S.SubmitContainer>
        <Link href="/">
          <S.CartButton $type="secondary">Continue Shopping</S.CartButton>
        </Link>
        <S.CartButton data-cy={CypressFields.CheckoutPlaceOrder} type="submit">Place Order</S.CartButton>
      </S.SubmitContainer>
    </S.CheckoutForm>
  );
};

export default CheckoutForm;
