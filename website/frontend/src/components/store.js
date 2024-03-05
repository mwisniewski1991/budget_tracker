import { writable } from "svelte/store"

export const userTypeId = writable('2');
export const userCategoryId = writable('02');
export const userSubcategoryId = writable('0001');

export const billTotalAmount = writable(0.0);

export const addPostionViewVisible = writable(true);
export const accountsBalanceViewVisible = writable(false);
export const expensesViewVisible = writable(false);

export const positionsOwnerID = writable('1');
export const positionsAccountID = writable('05');
