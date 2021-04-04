import axios from 'axios';

const API_URL = 'http://localhost:5000';

export async function getQuote(userId, stockSymbol, transNum) {
  let endpoint = `/get/QUOTE/trans/${transNum}/user/${userId}/stock/${stockSymbol.toUpperCase()}`;
  let resp = await axios.get(`${API_URL}${endpoint}`);
  return resp.data
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
    'stock_symbol': stockSymbol.toUpperCase(),
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
    'stock_symbol': stockSymbol.toUpperCase(),
    'transaction_num': 3
  };
  return await axios.post(`${API_URL}${endpoint}`, data);
}

export async function postTrigger(triggerType, userId, stockSymbol, price) {
  let endpoint = triggerType === 'SET_BUY_TRIGGER' ? '/set_buy_trigger' : '/set_sell_trigger';

  let data = {
    'command': triggerType,
    'user_id': userId,
    'amount': price,
    'stock_symbol': stockSymbol.toUpperCase(),
    'transaction_num': 3
  };
  return await axios.post(`${API_URL}${endpoint}`, data);
}

export async function postTriggerCancel(cancelType, userId, stockSymbol) {
  let endpoint = cancelType === 'CANCEL_SET_BUY' ? '/cancel_set_buy' : '/cancel_set_sell';

  let data = {
    'command': cancelType,
    'user_id': userId,
    'stock_symbol': stockSymbol.toUpperCase(),
    'transaction_num': 3
  };
  return await axios.post(`${API_URL}${endpoint}`, data);
}

export async function generateDumplog(userId, filename) {
  let endpoint = `/get/DUMPLOG/trans/${3}/file/${filename}`;

  let params = userId ? { userId: userId } : {};
  let resp = await axios.get(`${API_URL}${endpoint}`, { params });
  return resp.data
}

export async function getDisplaySummary(userId) {
  let endpoint = `/get/DISPLAY_SUMMARY/trans/${3}/user/${userId}`;
  return await axios.get(`${API_URL}${endpoint}`);
}