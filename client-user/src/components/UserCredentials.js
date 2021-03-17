import React, { useState } from 'react';

const UserCredentials = (props) => {
  return (
    <div className='user-credentials'>
      <input
        required id='user-id'
        name='user_id'
        placeholder='User Id'
        value={props.userId}
        onChange={val => props.onChangeUserId(val.target.value)}
      />
      <label id='admin'>Admin:</label>
      <input
        className='checkboxes'
        name='admin'
        type='checkbox'
        value={props.isAdmin}
        onChange={val => props.onChangeIsAdmin(val.target.checked)}
        checked={props.isAdmin}
      />
    </div>
  )
}

export default UserCredentials;