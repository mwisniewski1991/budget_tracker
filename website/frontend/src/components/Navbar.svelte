<script>
  import {accountsBalanceViewVisible ,positionsCockpitViewVisible } from './store';

  function changeAccountsBalanceViewVisible(){
    accountsBalanceViewVisible.set(true);
    positionsCockpitViewVisible.set(false);

  };

  function changePositionsCockpitViewVisible(){
    accountsBalanceViewVisible.set(false);
    positionsCockpitViewVisible.set(true);

  };


</script>


<nav class="navbar navbar-light p-2">
<!-- <nav class="navbar navbar-light bg-light"> -->


          <div class="navbar-nav">
            <button class="btn btn-sm btn-outline-secondary" type="button" on:click={changePositionsCockpitViewVisible}>Pozycje</button>
            <button class="btn btn-sm btn-outline-secondary" type="button" on:click={changeAccountsBalanceViewVisible}>Bilans kont</button>
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