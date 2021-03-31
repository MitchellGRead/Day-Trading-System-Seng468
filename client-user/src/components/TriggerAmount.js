import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { postTriggerAmount } from '../api';

const TriggerAmount = (props) => {
  const [loading, setLoading] = useState(false);
  const { register, handleSubmit } = useForm();
  const [triggerAmountType, setTriggerAmountType] = useState('SET_BUY_AMOUNT');
  const userId = props.userId;
  const onError = props.onError;
  const onSuccess = props.onSuccess;

  const getActionName = () => {
    return triggerAmountType.toLowerCase().replaceAll('_', ' ');
  };

  const onSubmit = async (data) => {
    onError('');
    onSuccess('');
    if (!userId) {
      onError('User id field must be specified');
      return
    }

    try {
      setLoading(true);
      let res = await postTriggerAmount(data.triggerAmount, userId, data.ticker, parseFloat(data.stock));
      if (res.status === 200) {
        onSuccess(`Successfully ${getActionName()} for ${data.ticker}`)
      }
    } catch (error) {
      if (error.response.status === 404) {
        let amountOrStock = triggerAmountType === 'SET_BUY_AMOUNT' ? 'stock to buy.' : 'stock to sell.'
        onError(`${userId} does not have enough ${amountOrStock} or ${userId} does not exist (add funds to account)`)
      } else {
        console.error(error);
        onError(`${error.message} - Failed to ${getActionName()}.`)
      }
    } finally {
      setLoading(false);
    }
  };

  const capitalizeWords = (val) => {
    let strs = val.split(' ');
    return strs.map(str => str.charAt(0).toUpperCase() + str.slice(1).toLowerCase()).join(' ');
  };

  return (
    <form className='trigger-amount-form right-space-content' onSubmit={handleSubmit(onSubmit)}>
      <select
        name='triggerAmount'
        onChange={val => setTriggerAmountType(val.target.value)}
        disabled={loading}
        ref={register}
      >
        <option value='SET_BUY_AMOUNT'>Buy Amount</option>
        <option value='SET_SELL_AMOUNT'>Sell Amount</option>
      </select>
      <input
        required
        placeholder={`Symbol to ${getActionName()}`}
        name='ticker'
        type='text'
        disabled={loading}
        ref={register}
      />
      <input
        required
        placeholder={triggerAmountType === 'SET_BUY_AMOUNT' ? 'Number of stock to buy' : 'Number of stock to sell'}
        name='stock'
        type='number'
        step='1'
        min='0'
        disabled={loading}
        ref={register}
      />
      <input
        type='submit'
        disabled={loading}
        value={loading ? 'Initializing...' : capitalizeWords(getActionName())}
      />
    </form>
  );
}

export default TriggerAmount;