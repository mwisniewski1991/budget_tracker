<script>
    export let isModifyMode = false;

    async function changeMode(){
        if(isModifyMode === true){
            isModifyMode = false;
        }else{
            isModifyMode = true;
        }
    };


</script>

<button type="button" class="btn btn-info" on:click={changeMode}>MODIFY</button>            


