import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { generateDumplog } from '../api';

const Dumplog = (props) => {
  const [loading, setLoading] = useState(false);
  const { register, handleSubmit } = useForm();
  const userId = props.userId;
  const isAdmin = props.isAdmin;
  const onError = props.onError;

  const onSubmit = async (data) => {
    onError('');
    if (!userId && !isAdmin) {
      onError('Admin access required to generate all user dumplogs')
      return;
    }

    try {
      setLoading(true);
      let file = await generateDumplog(userId, data.filename.replaceAll(' ', '_'));
      // TODO set and handle error
    } catch (error) {
      console.error(error);
      onError(`${error.message} - Failed to generate dumplog file`)
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className='dumplog right-space-content'>
      <h3>Generate Dumplog</h3>
      <form onSubmit={handleSubmit(onSubmit)}>
        <input
          required
          type='text'
          name='filename'
          placeholder='File name for dumplog'
          disabled={loading}
          ref={register}
        />
        <input
          type='submit'
          disabled={loading}
          value={loading ? 'Generating...' : 'Generate'}
        />
      </form>
    </div>
  );
};

export default Dumplog;