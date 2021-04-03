import React from 'react';
import TriggerAmount from './TriggerAmount';
import TriggerExecute from './TriggerExecute';
import TriggerCancel from './TriggerCancel';

const Trigger = (props) => {
  const userId = props.userId;
  const onError = props.onError;
  const onSuccess = props.onSuccess;

  return (
    <div className='trigger'>
      <h3>Triggers</h3>
      <TriggerAmount userId={userId} onSuccess={onSuccess} onError={onError} />
      <TriggerExecute userId={userId} onSuccess={onSuccess} onError={onError} />
      <TriggerCancel userId={userId} onSuccess={onSuccess} onError={onError} />
    </div>
  );
}

export default Trigger;