import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { postCommit } from '../api';

const TransactionCommit = (props) => {
  const [loading, setLoading] = useState(false);
  const { _, handleSubmit } = useForm();
  const userId = props.userId;
  const onError = props.onError;

  const commitBuy = async () => {
    onError('');
    if (!userId) {
      onError('User id field must be specified');
      return
    }

    try {
      setLoading(true);
      let res = await postCommit('COMMIT_BUY', userId)
    } catch (error) {
      console.error(error);
      onError(`${error.message} - Failed to commit buy.`);
    } finally {
      setLoading(false);
    }
  };

  const commitSell = async () => {
    onError('');
    if (!userId) {
      onError('User id field must be specified');
      return
    }

    try {
      setLoading(true);
      let res = await postCommit('COMMIT_SELL', userId)
    } catch (error) {
      console.error(error);
      onError(`${error.message} - Failed to commit sell.`);
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