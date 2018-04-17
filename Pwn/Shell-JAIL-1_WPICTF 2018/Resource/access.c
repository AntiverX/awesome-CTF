#include <sys/types.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <strings.h>
#include <string.h>

char *gen_cmd(int argc, const char **argv){
	size_t total_size = 1;
	for(int it = 1; it < argc; it++){
		total_size+= strlen(argv[it]);
	}
	char *ret = malloc(total_size);
	total_size = 0;
	for(int it = 1; it < argc; it++){
		size_t len = strlen(argv[it]);
		memcpy(ret+total_size, argv[it], len); 
		total_size+= len;
		ret[total_size] = ' ';
		total_size++;
	}
	ret[total_size] = '\0';
	return ret;
}

int filter(const char *cmd){
	int valid = 1;
	valid &= strstr(cmd, "*") == NULL;
	valid &= strstr(cmd, "sh") == NULL;
	valid &= strstr(cmd, "/") == NULL;
	valid &= strstr(cmd, "home") == NULL;
	valid &= strstr(cmd, "pc_owner") == NULL;
	valid &= strstr(cmd, "flag") == NULL;
	valid &= strstr(cmd, "txt") == NULL;
	return valid;
}


int main(int argc, const char **argv){
	setreuid(UID, UID);
	char *cmd = gen_cmd(argc, argv);
	if (!filter(cmd)){
		exit(-1);
	}
	system(cmd);
}
