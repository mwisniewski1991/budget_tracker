<script>
  import {addPostionViewVisible, accountsBalanceViewVisible, expensesViewVisible } from './store';

  function changeAddPostionViewVisible(){
    addPostionViewVisible.set(true);
    accountsBalanceViewVisible.set(false);
    expensesViewVisible.set(false);

  };
  function changeAccountsBalanceViewVisible(){
    addPostionViewVisible.set(false);
    accountsBalanceViewVisible.set(true);
    expensesViewVisible.set(false);

  };

  function changeExpensesViewVisible(){
    addPostionViewVisible.set(false);
    accountsBalanceViewVisible.set(false);
    expensesViewVisible.set(true);

  };


</script>


<nav class="navbar navbar-light bg-light">

          <div class="navbar-nav">
            <button class="btn btn-sm btn-outline-secondary" type="button" on:click={changeAddPostionViewVisible}>Dodaj pozycje</button>
            <button class="btn btn-sm btn-outline-secondary" type="button" on:click={changeAccountsBalanceViewVisible}>Bilans kont</button>
            <button class="btn btn-sm btn-outline-secondary" type="button" on:click={changeExpensesViewVisible}>Wydatki</button>
          </div>

  </nav>