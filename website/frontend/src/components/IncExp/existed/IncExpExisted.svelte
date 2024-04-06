<script>
    import DeleteHeaderButton from "./components/buttons/DeleteHeaderButton.svelte";
    import ModifyHeaderButton from "./components/buttons/ModifyHeaderButton.svelte";
    import PostHeaderButton from "./components/buttons/PostHeaderButton.svelte";
    import Header from "./components/Header.svelte";
    import Positions from "./components/Positions.svelte";
    
    export let IncExp;

    let currentTypeId;
    let isModifyMode;

</script>

<div class="container container-border">
    
    <form action="/modify" method="post">
            <div>
                <span>{IncExp['header_id']}</span>
                <DeleteHeaderButton headerIDtoDelete={IncExp['header_id']}/>
                <ModifyHeaderButton bind:isModifyMode/>
                <PostHeaderButton isModifyMode={isModifyMode}/>
            </div>
            
            <Header 
                bind:currentTypeId
                isModifyMode={isModifyMode}
                IncExp={IncExp}
                />

            
            {#each IncExp['positions'] as position }
                <Positions 
                    isModifyMode={isModifyMode}
                    currentTypeId={currentTypeId}
                    PositionData={position} 
                    typeId = {IncExp['type_id']}
                    />
            {/each}

        </form>

</div>

<style>
    .container-border{
        border: 1px solid white;
        padding: 5px 5px;
        margin-bottom: 20px;
    }
</style>