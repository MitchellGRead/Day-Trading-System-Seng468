import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { postTriggerCancel } from '../api';

const TriggerCancel = (props) => {
  const [loading, setLoading] = useState(false);
  const [stockSymbol, setStockSymbol] = useState('');
  const { _, handleSubmit } = useForm();
  const userId = props.userId;
  const onError = props.onError;
  const onSuccess = props.onSuccess;

  const cancelBuy = async () => {
    onError('');
    onSuccess('');
    if (!userId) {
      onError('User id field must be specified');
      return
    }

    try {
      setLoading(true);
      let res = await postTriggerCancel('CANCEL_SET_BUY', userId, stockSymbol);
      if (res.status === 200) {
        onSuccess(`Successfully cancelled buy trigger for ${stockSymbol}.`)
      }
    } catch (error) {
      let status = error.response.status;
      if (status === 404) {
        onError(`No buy trigger to cancel or ${userId} does not exist (add funds to account).`)
      } else if (status === 400) {
        onError(error.response.data.errorMessage);
      } else {
        console.error(error);
        onError(`${error.message} - Failed to cancel buy trigger.`);
      }
    } finally {
      setLoading(false);
    }
  };

  const cancelSell = async () => {
    onError('');
    onSuccess('');
    if (!userId) {
      onError('User id field must be specified');
      return
    }

    try {
      setLoading(true);
      let res = await postTriggerCancel('CANCEL_SET_SELL', userId, stockSymbol);
      if (res.status === 200) {
        onSuccess(`Successfully cancelled sell trigger for ${stockSymbol}.`)
      }
    } catch (error) {
      let status = error.response.status;
      if (status === 404) {
        onError(`No sell trigger to cancel or ${userId} does not exist (add funds to account).`)
      } else if (status === 400) {
        onError(error.response.data.errorMessage);
      } else {
        console.error(error);
        onError(`${error.message} - Failed to cancel sell trigger.`);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className='cancel-form right-space-content'>
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