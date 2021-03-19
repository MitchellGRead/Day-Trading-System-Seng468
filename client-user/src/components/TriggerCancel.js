import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { postTriggerCancel } from '../api';

const TriggerCancel = (props) => {
  const [loading, setLoading] = useState(false);
  const [stockSymbol, setStockSymbol] = useState('');
  const { _, handleSubmit } = useForm();
  const userId = props.userId;
  const onError = props.onError;

  const cancelBuy = async () => {
    onError('');
    if (!userId) {
      onError('User id field must be specified');
      return
    }

    try {
      setLoading(true);
      let res = await postTriggerCancel('CANCEL_SET_BUY', userId, stockSymbol);
    } catch (error) {
      console.error(error);
      onError(`${error.message} - Failed to cancel buy trigger.`);
    } finally {
      setLoading(false);
    }
  };

  const cancelSell = async () => {
    onError('');
    if (!userId) {
      onError('User id field must be specified');
      return
    }

    try {
      setLoading(true);
      let res = await postTriggerCancel('CANCEL_SET_SELL', userId, stockSymbol);
    } catch (error) {
      console.error(error);
      onError(`${error.message} - Failed to cancel sell trigger.`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className='cancel-form'>
      <input
        required
        name='stockSymbol'
        type='text'
        placeholder='Symbol to cancel trigger for'
        value={stockSymbol}
        onChange={val => setStockSymbol(val.target.value)}
        disabled={loading}
      />
      <input
        name='cancelBuyTrigger'
        type='button'
        disabled={loading}
        value={loading ? 'Cancelling...' : 'Cancel Buy Trigger'}
        onClick={handleSubmit(cancelBuy)}
      />
      <input
        name='cancelSellTrigger'
        type='button'
        disabled={loading}
        value={loading ? 'Cancelling...' : 'Cancel Sell Trigger'}
        onClick={handleSubmit(cancelSell)}
      />
    </form>
  );
}

export default TriggerCancel;