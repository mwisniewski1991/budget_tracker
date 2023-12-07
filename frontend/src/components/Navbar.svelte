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

    <div class="container-fluid">

        <span class="navbar-brand">Menu</span>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarNavAltMarkup">

          <div class="navbar-nav">
            <button class="btn btn-sm btn-outline-secondary" type="button" on:click={changeAddPostionViewVisible}>Dodaj pozycje</button>
            <button class="btn btn-sm btn-outline-secondary" type="button" on:click={changeAccountsBalanceViewVisible}>Bilans kont</button>
            <button class="btn btn-sm btn-outline-secondary" type="button" on:click={changeExpensesViewVisible}>Wydatki</button>
          </div>

        </div>
        
    </div>

  </nav>