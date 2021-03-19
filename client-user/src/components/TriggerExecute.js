import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { postTrigger } from '../api';

const TriggerExecute = (props) => {
  const [loading, setLoading] = useState(false);
  const { register, handleSubmit } = useForm();
  const [triggerType, setTriggerType] = useState('SET_BUY_TRIGGER');
  const userId = props.userId;
  const onError = props.onError;

  const getActionName = () => {
    return triggerType.toLowerCase().replaceAll('_', ' ');
  };

  const onSubmit = async (data) => {
    onError('');
    if (!userId) {
      onError('User id field must be specified');
      return
    }

    try {
      setLoading(true);
      let res = await postTrigger(data.trigger, userId, data.ticker, data.price);
      // TODO set and handle error
    } catch (error) {
      console.error(error);
      onError(`${error.message} - Failed to ${getActionName()}.`)
    } finally {
      setLoading(false);
    }
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
        value={loading ? 'Initializing...' : getActionName().toUpperCase()}
      />
    </form>
  );
}

export default TriggerExecute;