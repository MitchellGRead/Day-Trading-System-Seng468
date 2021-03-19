import React from 'react';
import TriggerAmount from './TriggerAmount';
import TriggerExecute from './TriggerExecute';
import TriggerCancel from './TriggerCancel';

const Trigger = (props) => {
  const userId = props.userId;
  const onError = props.onError;

  return (
    <div className='trigger'>
      <h3>Triggers</h3>
      <TriggerAmount userId={userId} onError={onError} />
      <TriggerExecute userId={userId} onError={onError} />
      <TriggerCancel userId={userId} onError={onError} />
    </div>
  );
}

export default Trigger;