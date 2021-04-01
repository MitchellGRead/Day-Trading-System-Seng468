import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { postTrigger } from '../api';

const TriggerExecute = (props) => {
  const [loading, setLoading] = useState(false);
  const { register, handleSubmit } = useForm();
  const [triggerType, setTriggerType] = useState('SET_BUY_TRIGGER');
  const userId = props.userId;
  const onError = props.onError;
  const onSuccess = props.onSuccess;

  const getActionName = () => {
    return triggerType.toLowerCase().replaceAll('_', ' ');
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
      let res = await postTrigger(data.trigger, userId, data.ticker, parseFloat(data.price));
      if (res.status === 200) {
        onSuccess(`Trigger creation was successful for ${data.ticker}`)
      }
    } catch (error) {
      if (error.response.status === 404) {
        onError(`Failed to create trigger due to no amount set, insufficient funds/stock, or ${userId} does not exist (add funds to account).`)
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
    <form className='trigger-form right-space-content' onSubmit={handleSubmit(onSubmit)}>
      <select
        name='trigger'
        onChange={val => setTriggerType(val.target.value)}
        disabled={loading}
        ref={register}
      >
        <option value='SET_BUY_TRIGGER'>Buy Trigger</option>
        <option value='SET_SELL_TRIGGER'>Sell Trigger</option>
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
        placeholder='Quote execution price'
        name='price'
        type='number'
        step='0.01'
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

export default TriggerExecute;