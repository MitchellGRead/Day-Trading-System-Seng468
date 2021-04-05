import React from 'react';

const Success = (props) => {
  const success = props.success || '';

  return (
    <div className='success'>
      <h3>{success}</h3>
    </div>
  )
}

export default Success