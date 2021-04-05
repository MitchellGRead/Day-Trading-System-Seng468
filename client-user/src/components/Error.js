import React from 'react';

const Error = (props) => {
  const error = props.error || '';

  return (
    <div className='error'>
      <h3>{error}</h3>
    </div>
  )
}

export default Error