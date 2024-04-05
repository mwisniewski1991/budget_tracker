<script>
  import {addPostionViewVisible, accountsBalanceViewVisible ,positionsCockpitViewVisible } from './store';

  function changeAddPostionViewVisible(){
    addPostionViewVisible.set(true);
    accountsBalanceViewVisible.set(false);
    positionsCockpitViewVisible.set(false);

  };
  function changeAccountsBalanceViewVisible(){
    addPostionViewVisible.set(false);
    accountsBalanceViewVisible.set(true);
    positionsCockpitViewVisible.set(false);

  };

  function changePositionsCockpitViewVisible(){
    addPostionViewVisible.set(false);
    accountsBalanceViewVisible.set(false);
    positionsCockpitViewVisible.set(true);

  };


</script>


<nav class="navbar navbar-light bg-light">

          <div class="navbar-nav">
            <button class="btn btn-sm btn-outline-secondary" type="button" on:click={changeAddPostionViewVisible}>Dodaj pozycje</button>
            <button class="btn btn-sm btn-outline-secondary" type="button" on:click={changeAccountsBalanceViewVisible}>Bilans kont</button>
            <button class="btn btn-sm btn-outline-secondary" type="button" on:click={changePositionsCockpitViewVisible}>Wydatki</button>
          </div>

  </nav>