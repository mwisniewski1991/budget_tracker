import { writable } from "svelte/store"

export const userTypeId = writable('2');
export const userCategoryId = writable('02');
export const userSubcategoryId = writable('0001');

export const billTotalAmount = writable(0.0);

export const positionsCockpitViewVisible = writable(true);
export const accountsBalanceViewVisible = writable(false);

export const incexpList = writable([]);
export const incexpExistedList = writable([]);
export const CategoriesSubcategoriesList = writable([]);

// PositionsCockpit
export const activeOnwerId = writable(localStorage.getItem("activeOnwerIdLocalData") ? localStorage.getItem("activeOnwerIdLocalData") :'2');
export const activeAccountId = writable(localStorage.getItem("activeAccountIdLocalData") ? localStorage.getItem("activeAccountIdLocalData") :'04');

// IncExpNew
export const IncExpNewTypeId = writable('2');
export const IncExpNewTotalBillValue = writable(0.00);

export const IncExpNewTypeIdDefault = writable('2');
export const IncExpNewCategoryIdDefault = writable('02');
export const IncExpNewSubcategoryIdDefault = writable('0001');

// IncExpFilters
export const incExpFilterLimitValue = writable(50); 
// export const incExpFilterDetailsVisible = writable(false);
export const incExpFilterDetailsVisible = writable(localStorage.getItem("incExpFilterDetailsVisibleLocalData") ? localStorage.getItem("incExpFilterDetailsVisibleLocalData") : false);