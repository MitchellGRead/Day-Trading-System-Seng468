import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { postCommit } from '../api';

const TransactionCommit = (props) => {
  const [loading, setLoading] = useState(false);
  const { _, handleSubmit } = useForm();
  const userId = props.userId;
  const onError = props.onError;
  const onSuccess = props.onSuccess;

  const commitBuy = async () => {
    onError('');
    onSuccess('');
    if (!userId) {
      onError('User id field must be specified');
      return
    }

    try {
      setLoading(true);
      let res = await postCommit('COMMIT_BUY', userId)
      if (res.status === 200) {
        onSuccess('Successfully purchased stock.')
      }
    } catch (error) {
      if (error.response.status === 404) {
        onError('No BUY exists to commit.')
      } else {
        console.error(error);
        onError(`${error.message} - Failed to commit buy.`);
      }
    } finally {
      setLoading(false);
    }
  };

  const commitSell = async () => {
    onError('');
    onSuccess('');
    if (!userId) {
      onError('User id field must be specified');
      return
    }

    try {
      setLoading(true);
      let res = await postCommit('COMMIT_SELL', userId)
      if (res.status === 200) {
        onSuccess('Successfully sold stock')
      }
    } catch (error) {
      if (error.response.status === 404) {
        onError('No SELL exists to commit.')
      } else {
        console.error(error);
        onError(`${error.message} - Failed to commit buy.`);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className='commit-form right-space-content'>
      <input
        name='commitBuy'
        type='button'
        disabled={loading}
        value={loading ? 'Committing...' : 'Commit Buy'}
        onClick={handleSubmit(commitBuy)}
      />
      <input
        name='commitSell'
        type='button'
        disabled={loading}
        value={loading ? 'Committing...' : 'Commit Sell'}
        onClick={handleSubmit(commitSell)}
      />
    </form>
  );
}

export default TransactionCommit;