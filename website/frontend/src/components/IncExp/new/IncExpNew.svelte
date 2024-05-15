<script>
    import Header from "./components/Header.svelte"
    import Positions from "./components/Positions.svelte";
    import {range} from "./components/range";

    let newPostitsionCounter = 1;
    let currentTypeId;

    const addPosition = () => (newPostitsionCounter<10) ? newPostitsionCounter += 1 : newPostitsionCounter; 
    const removePosition = () => (newPostitsionCounter>1) ? newPostitsionCounter -= 1 : newPostitsionCounter; 

</script>

<div class="container container-border">
    <h3>Dodaj nowy rekord</h3>
    
    <form action="/add" method="post" class="IncExpNew">
     

        <Header bind:currentTypeId/>

        {#each range(1, newPostitsionCounter + 1, 1) as i}
            <Positions positionId={i} currentTypeId={currentTypeId}/>
        {/each}
        <div>
            <button type="submit" class="btn btn-primary" >Prześlij</button>
            <button class="btn btn-secondary" type="button" on:click={addPosition}>Dodaj pozycję</button>
            <button class="btn btn-secondary" type="button" on:click={removePosition}>Usuń pozycję</button>
        </div>
    </form>
</div>


<style>
    .container-border{
        border: 1px solid white;
        border-radius: 10px;
        padding: 5px 5px;
        margin-bottom: 20px;
    }
    /* .income-position{
        color: green;
    }
    .expense-position{
        color: red;
    } */

</style>