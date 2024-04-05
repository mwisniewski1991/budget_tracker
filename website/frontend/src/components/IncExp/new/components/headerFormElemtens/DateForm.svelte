<script>
    import { onMount } from 'svelte';

    let currentDateString;

    onMount(()=> {
        let now = new Date(), month, day, year;
        
        month = '' + (now.getMonth() + 1),
        day = '' + now.getDate(),
        year = now.getFullYear();

        if (month.length < 2) month = '0' + month;
        if (day.length < 2) day = '0' + day;

        currentDateString = [year, month, day].join('-');
	})

</script>

<input type="date" class="form-control" id="date" name="date" bind:value={currentDateString}>