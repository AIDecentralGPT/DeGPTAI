
<script lang="ts">
  import { showSidebar } from "$lib/stores";
  import MenuLines from "$lib/components/icons/MenuLines.svelte";

</script>
<div class='w-full bg-zinc-950'>
	<div
		class="{$showSidebar
		? 'md:hidden'
		: ''} mr-3 self-start flex flex-none items-center text-gray-600 dark:text-gray-400"
	>
		<button
			id="sidebar-toggle-button"
			class="cursor-pointer px-2 py-2 flex rounded-xl hover:bg-gray-100 dark:hover:bg-gray-850 transition"
			on:click={() => {
				showSidebar.set(!$showSidebar);
			}}
		>
			<div class=" m-auto self-center">
				<MenuLines />
			</div>
		</button>
	</div>

	<div class="h-[80vh] flex flex-wrap flex-col items-center justify-center  text-white break-words ">

		<h1 class="leading-none font-bold mb-16 text-[7vw]">
		  DecentralGPT AI
		</h1>
	  
		<div class="items-center flex-col">
		  <!-- <a class="items-center gap-[0.38rem] cursor-pointer flex justify-center py-3.5 px-8 rounded-full" href=" ">
			<span>Get Started</span>
		  </a > -->
	  
		  <a class="mb-5 flex-1 items-center bg-white text-zinc-950 gap-[0.38rem] cursor-pointer flex justify-center py-3.5 px-8 rounded-full" href="https://www.decentralgpt.org/wp-content/uploads/2024/06/degptv1.0_0712.apk">
			<span class="flex">
			  <svg class="h-3 w-5" fill="none" height="11" viewBox="0 0 18 11" width="18" xmlns="http://www.w3.org/2000/svg">
				<path
				  d="M17.9438 10.0029C17.7953 8.68298 17.3538 7.41236 16.6511 6.28276C15.9484 5.15316 15.0021 4.19279 13.8805 3.47101L14.8836 1.47542C14.9894 1.24085 14.9999 0.974764 14.913 0.732674C14.8261 0.490583 14.6486 0.291192 14.4174 0.176107C14.1861 0.0610207 13.9192 0.0391302 13.6721 0.115003C13.425 0.190875 13.217 0.35865 13.0914 0.583318L12.0843 2.58555L11.8221 2.48185C10.9029 2.17859 9.94046 2.02461 8.97191 2.02583C7.97682 2.02583 7.01917 2.18537 6.12305 2.48185L5.8609 2.58555L4.85377 0.583318C4.79786 0.461479 4.71783 0.352082 4.61846 0.261656C4.51909 0.171229 4.40242 0.101626 4.2754 0.0569982C4.14838 0.0123704 4.01362 -0.00636709 3.87915 0.00190356C3.74469 0.0101742 3.61328 0.0452836 3.49277 0.105137C3.37225 0.16499 3.2651 0.248361 3.1777 0.350275C3.09031 0.452189 3.02446 0.570558 2.98409 0.698319C2.94372 0.826081 2.92965 0.960617 2.94272 1.0939C2.9558 1.22718 2.99575 1.35649 3.06019 1.47409L4.06331 3.47101C2.94181 4.19286 1.99556 5.15325 1.29287 6.28283C0.590182 7.41242 0.148598 8.68301 0 10.0029V11H18V10.0029H17.9438ZM5.96255 8.00861C5.69651 8.00896 5.44122 7.90425 5.25284 7.7175C5.06447 7.53075 4.95845 7.27727 4.95809 7.01281C4.95774 6.74836 5.06308 6.49459 5.25095 6.30734C5.43882 6.1201 5.69383 6.0147 5.95987 6.01435H5.96522C6.23127 6.01453 6.48635 6.11975 6.67434 6.30687C6.86234 6.494 6.96785 6.74769 6.96768 7.01215C6.9675 7.2766 6.86164 7.53016 6.6734 7.71703C6.48515 7.9039 6.22993 8.00879 5.96389 8.00861H5.96255ZM11.9813 8.00861C11.7152 8.00896 11.4599 7.90425 11.2716 7.7175C11.0832 7.53075 10.9772 7.27727 10.9768 7.01281C10.9765 6.74836 11.0818 6.49459 11.2697 6.30734C11.4575 6.1201 11.7126 6.0147 11.9786 6.01435H11.984C12.25 6.01453 12.5051 6.11975 12.6931 6.30687C12.8811 6.494 12.9866 6.74769 12.9864 7.01215C12.9862 7.2766 12.8804 7.53016 12.6921 7.71703C12.5039 7.9039 12.2487 8.00879 11.9826 8.00861H11.9813Z"
				  fill="rgb(8, 8, 8)"
				/>
			  </svg>
			</span>
	  
			<span>Android</span>
		  </a >
	  
		  <a class="mb-5 flex-1 items-center bg-white text-zinc-950 gap-[0.38rem] cursor-pointer flex justify-center py-3.5 px-8 rounded-full" href="https://play.google.com/store">
			<span class="flex">
			  <svg class="h-5 w-5" fill="none" height="19" viewBox="0 0 19 19" width="19" xmlns="http://www.w3.org/2000/svg">
				<path d="M12.0072 8.78433L4.7262 1.48438L13.9887 6.802L12.0064 8.78433H12.0072Z" fill="rgb(8, 8, 8)" />
				<path d="M2.8262 1.05518C2.3987 1.28001 2.11133 1.68851 2.11133 2.21972V16.7769C2.11133 17.3073 2.39791 17.7166 2.82699 17.9406L11.2915 9.49672L2.8262 1.05518Z" fill="rgb(8, 8, 8)" />
				<path d="M16.853 8.49697L14.9095 7.3728L12.7427 9.50001L14.9095 11.6272L16.8926 10.5031C17.4863 10.0312 17.4863 8.9688 16.853 8.49697Z" fill="rgb(8, 8, 8)" />
				<path d="M4.7262 17.5155L13.9887 12.1979L12.0072 10.2156L4.7262 17.5155Z" fill="rgb(8, 8, 8)" />
			  </svg>
			</span>
	  
			<span>Google Play</span>
		  </a >
	  
		  <a class="mb-5 flex-1 items-center bg-white text-zinc-950 gap-[0.38rem] cursor-pointer flex justify-center py-3.5 px-8 rounded-full" href="https://apps.apple.com/us/app/degpt/id6504377109?platform=iphone">
			<span class="flex">
			  <svg class="h-4 w-4" fill="none" height="17" viewBox="0 0 17 17" width="17" xmlns="http://www.w3.org/2000/svg">
				<path d="M13.14 9.03271C13.1185 6.87981 14.8958 5.8473 14.9752 5.796C13.9766 4.33474 12.421 4.13456 11.8667 4.11141C10.5429 3.97738 9.28358 4.89082 8.61171 4.89082C7.94155 4.89082 6.90479 4.13124 5.80687 4.15119C4.36394 4.17264 3.03346 4.9902 2.29048 6.28249C0.791305 8.8839 1.90656 12.7378 3.36775 14.8476C4.08174 15.8803 4.93313 17.0403 6.05098 16.9988C7.12745 16.9559 7.53451 16.3023 8.83597 16.3023C10.1374 16.3023 10.5032 16.9988 11.6424 16.9774C12.8008 16.9559 13.5347 15.9249 14.2438 14.889C15.0637 13.6909 15.4013 12.531 15.4212 12.4714C15.3955 12.4597 13.1624 11.6042 13.14 9.03271ZM10.9995 2.7147C11.5928 1.9949 11.9933 0.996253 11.884 0C11.0294 0.0347966 9.99349 0.569264 9.38036 1.28744C8.83016 1.92454 8.34862 2.94138 8.47767 3.91771C9.43169 3.99215 10.4056 3.43288 10.9995 2.7147Z" fill="rgb(8, 8, 8)" />
			  </svg>
			</span>
	  
			<span>App Store</span>
		  </a >
		</div>
	</div>
</div>

