import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { getQuote } from '../api';

const Quote = (props) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [quote, setQuote] = useState(0.0);
  const { register, handleSubmit } = useForm();
  const userId = props.userId

  const onSubmit = async (data) => {
    setError('');
    if (!userId) {
      setError('User id field must be specified');
      return
    }

    try {
      setLoading(true);

      let quotePrice = await getQuote(userId, data.ticker, 3);
      setQuote(quotePrice);
    } catch (error) {
      console.error(error);
      setError(error);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className='quote'>
      <form onSubmit={handleSubmit(onSubmit)}>

        <input
          required
          name='ticker'
          type='text'
          placeholder='Ticker symbol'
          disabled={loading}
          ref={register}
        />
        <input
          type='submit'
          disabled={loading}
          value={loading ? 'Fetching...' : 'Quote'}
        />
      </form>
      {error && <h3 className='error'>{error}</h3>}
      {
        quote !== 0 &&
        <p>Quote Price: {quote}</p>
      }
    </div>
  )
}

export default Quote;