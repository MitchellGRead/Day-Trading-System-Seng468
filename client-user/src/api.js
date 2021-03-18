import axios from 'axios';

const API_URL = 'https://localhost:5000';

// TODO get this actually hooked up
export async function getQuote(userId, stockSymbol, transNum) {
  let endpoint = `/get/QUOTE/trans/${transNum}/user_id/${userId}/stock_symbol/${stockSymbol}`;
  return await axios.get(`${API_URL}${endpoint}`);
}

export async function postFunds(userId, funds) {
  let endpoint = `/add`;
  let data = {
    'user_id': userId,
    'amount': funds,
    'command': 'ADD',
    'transaction_num': 3
  };
  return await axios.post(`${API_URL}${endpoint}`, data);
}

export async function postTransact(transactType, userId, stockSymbol, funds) {
  let endpoint = transactType === 'BUY' ? '/buy' : '/sell';

  let data = {
    'command': transactType,
    'user_id': userId,
    'stock_symbol': stockSymbol,
    'amount': funds,
    'transaction_num': 3
  };
  return await axios.post(`${API_URL}${endpoint}`, data);
}

export async function postCommit(commitType, userId) {
  let endpoint = commitType === 'COMMIT_BUY' ? '/commit_buy' : '/commit_sell';

  let data = {
    'command': commitType,
    'user_id': userId,
    'transaction_num': 3
  };
  return await axios.post(`${API_URL}${endpoint}`, data);
}

export async function postCancel(cancelType, userId) {
  let endpoint = cancelType === 'CANCEL_BUY' ? '/cancel_buy' : '/cancel_sell';

  let data = {
    'command': cancelType,
    'user_id': userId,
    'transaction_num': 3
  };
  return await axios.post(`${API_URL}${endpoint}`, data);
}

export async function postTriggerAmount(triggerType, userId, stockSymbol, funds) {
  let endpoint = triggerType === 'SET_BUY_AMOUNT' ? '/set_buy_amount' : '/set_sell_amount';

  let data = {
    'command': triggerType,
    'user_id': userId,
    'amount': funds,
    'stock_symbol': stockSymbol,
    'transaction_num': 3
  };
  return await axios.post(`${API_URL}${endpoint}`, data);
}