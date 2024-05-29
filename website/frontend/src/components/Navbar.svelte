<script>
  import {accountsBalanceViewVisible ,positionsCockpitViewVisible, onwersAccountsCreatorViewVisible } from './store';

  function changeAccountsBalanceViewVisible(){
    accountsBalanceViewVisible.set(true);
    positionsCockpitViewVisible.set(false);
    onwersAccountsCreatorViewVisible.set(false);


  };

  function changePositionsCockpitViewVisible(){
    accountsBalanceViewVisible.set(false);
    positionsCockpitViewVisible.set(true);
    onwersAccountsCreatorViewVisible.set(false);

  };

  function changeOnwersAccountsCreatorViewVisible(){
    accountsBalanceViewVisible.set(false);
    positionsCockpitViewVisible.set(false);
    onwersAccountsCreatorViewVisible.set(true);

  };


</script>


<nav class="navbar navbar-light p-2">
<!-- <nav class="navbar navbar-light bg-light"> -->


          <div class="navbar-nav">
            <button class="btn btn-sm btn-outline-secondary" type="button" on:click={changePositionsCockpitViewVisible}>Pozycje</button>
            <button class="btn btn-sm btn-outline-secondary" type="button" on:click={changeAccountsBalanceViewVisible}>Bilans kont</button>
            <button class="btn btn-sm btn-outline-secondary" type="button" on:click={changeOnwersAccountsCreatorViewVisible}>Właściciele i konta</button>
            <a class="nav-link active" aria-current="page" href="/accounts-results">Bilans kont</a>
            <a class="nav-link active" aria-current="page" href="/owners">Właściciele</a>
          </div>

  </nav>

<style>
  *{
		background-color:#131516;
		color: #fff;
	}
  nav{
    border: #fff solid 1px;
    border-radius: 10px;
		background-color:#131516;
  }
</style>