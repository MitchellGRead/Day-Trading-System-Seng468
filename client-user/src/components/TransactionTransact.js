import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { postTransact } from '../api';

const TransactionTransact = (props) => {
  const [loading, setLoading] = useState(false);
  const { register, handleSubmit } = useForm();
  const [transactType, setTransactType] = useState('BUY');
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
      let res = await postTransact(data.transact, userId, data.ticker, parseFloat(data.funds));
      if (res.status === 200) {
        onSuccess(`${capitalize(data.transact)} for ${data.ticker} was successfully initialized.`)
      }
    } catch (error) {
      let status = error.response.status;
      if (status === 404) {
        let fundsStock = data.transact === 'BUY' ? 'funds' : 'stock'
        onError(`Not enough ${fundsStock} to perform ${data.transact} or ${userId} does not exist (add funds to account)`)
      } else if (status === 400) {
        onError(error.response.data.errorMessage);
      } else {
        console.error(error)
        onError(`${error.message} - Failed to initialize ${transactType.toLowerCase()}.`)
      }

    } finally {
      setLoading(false);
    }
  }

  const capitalize = (val) => {
    return val.charAt(0).toUpperCase() + val.slice(1).toLowerCase();
  };

  return (
    <form className='transact-form right-space-content' onSubmit={handleSubmit(onSubmit)}>
      <select
        name='transact'
        onChange={val => setTransactType(val.target.value)}
        disabled={loading}
        ref={register}
      >
        <option value='BUY'>Buy</option>
        <option value='SELL'>Sell</option>
      </select>
      <input
        required
        placeholder={`Symbol to ${transactType.toLowerCase()}`}
        name='ticker'
        type='text'
        disabled={loading}
        ref={register}
        maxLength={3}
      />
      <input
        required
        placeholder='Funds to use'
        name='funds'
        type='number'
        step='0.01'
        min='0'
        disabled={loading}
        ref={register}
      />
      <input
        type='submit'
        disabled={loading}
        value={loading ? 'Initializing...' : capitalize(transactType)}
      />
    </form>
  );
}

export default TransactionTransact;