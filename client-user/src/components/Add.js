import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { postFunds } from '../api';

const Add = (props) => {
  const [loading, setLoading] = useState(false);
  const { register, handleSubmit } = useForm();
  const userId = props.userId;
  const onError = props.onError;
  const onSuccess = props.onSuccess;

  const onSubmit = async (data) => {
    onError('');
    onSuccess('');
    if (!userId) {
      onError('User id field must be specified');
      return
    }

    try {
      setLoading(true);
      let res = await postFunds(userId, parseFloat(data.funds))
      if (res.status === 200) {
        onSuccess(`Success adding $${data.funds} for ${userId}`)
      }
    } catch (error) {
      console.error(error);
      onError(`${error.message} - Failed to add funds.`)
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className='add right-space-content'>
      <h3>Add Funds</h3>
      <form onSubmit={handleSubmit(onSubmit)}>
        <input
          required
          name='funds'
          type='number'
          step='0.01'
          min='0'
          placeholder='Amount to add'
          disabled={loading}
          ref={register}
        />
        <input
          type='submit'
          disabled={loading}
          value={loading ? 'Adding Funds...' : 'Add'}
        />
      </form>
    </div>
  )
}

export default Add