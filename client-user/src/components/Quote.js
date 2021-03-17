import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { getQuote } from '../api';

const Quote = (props) => {
  const [loading, setLoading] = useState(false);
  const [quote, setQuote] = useState(0.0);
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

      let quotePrice = await getQuote(userId, data.ticker, 3);
      setQuote(quotePrice);
    } catch (error) {
      console.error(error);
      onError(`${error.message} - Failed to get quote.`);
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
      {
        quote !== 0 &&
        <p>Quote Price: {quote}</p>
      }
    </div>
  )
}

export default Quote;