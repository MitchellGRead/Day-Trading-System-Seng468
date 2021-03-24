import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { postCancel } from '../api';

const TransactionCancel = (props) => {
  const [loading, setLoading] = useState(false);
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
      let res = await postCancel('CANCEL_BUY', userId)
    } catch (error) {
      if (error.response.status === 404) {
        onError('No BUY to cancel.')
      } else {
        console.error(error);
        onError(`${error.message} - Failed to cancel buy.`);
      }
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
      let res = await postCancel('CANCEL_SELL', userId)
    } catch (error) {
      if (error.response.status === 404) {
        onError('No SELL to cancel.')
      } else {
        console.error(error);
        onError(`${error.message} - Failed to cancel sell.`);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className='cancel-form right-space-content'>
      <input
        name='cancelBuy'
        type='button'
        disabled={loading}
        value={loading ? 'Cancelling...' : 'Cancel Buy'}
        onClick={handleSubmit(cancelBuy)}
      />
      <input
        name='cancelSell'
        type='button'
        disabled={loading}
        value={loading ? 'Cancelling...' : 'Cancel Sell'}
        onClick={handleSubmit(cancelSell)}
      />
    </form>
  );
}

export default TransactionCancel;