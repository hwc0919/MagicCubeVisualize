export const getCube = function(url) {
    return fetch(url)
        .then((resp) => {
            return resp.json();
        })
        .then((data) => {
            console.log(data);
            if (data.success) this.cube = data.cube;
            else throw data.message || 'Failed';
        });
};
