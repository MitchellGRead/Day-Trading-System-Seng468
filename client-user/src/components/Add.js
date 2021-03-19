import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { postFunds } from '../api';

const Add = (props) => {
  const [loading, setLoading] = useState(false);
  const { register, handleSubmit } = useForm();
  const userId = props.userId;
  const onError = props.onError;

  const onSubmit = async (data) => {
    onError('');
    if (!userId) {
      onError('User id field must be specified');
      return
    }

    try {
      setLoading(true);
      let res = await postFunds(userId, data.postFunds)
      // TODO set and handle error
    } catch (error) {
      console.error(error);
      onError(`${error.message} - Failed to add funds.`)
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className='add'>
      <h3>Add Funds</h3>
      <form onSubmit={handleSubmit(onSubmit)}>
        <input
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