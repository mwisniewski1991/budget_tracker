import { writable } from "svelte/store"

export const userOwnerId = writable('');
export const userAccountId = writable('');

export const userTypeId = writable('2');
export const userCategoryId = writable('02');
export const userSubcategoryId = writable('0001');

export const billTotalAmount = writable(0.0);

export const addPostionViewVisible = writable(false);
export const accountsBalanceViewVisible = writable(true);
export const expensesViewVisible = writable(false);