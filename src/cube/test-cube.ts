import { Cube } from './cube'

let c = new Cube();
console.log('valid:', c.isValid());

for (let op in Cube.operations) {
    console.log(`\n${Cube.operations[op]} 4 times`);
    for (let i = 0; i < 4; i++) {
        c.takeOperation(op);
        console.log('valid:', c.isValid());
    }
    console.log('reset:', c.isReset());
}

for (let i = 0; i < 100; i++) {
    let index = Math.floor(Math.random() * Cube.opNames.length);
    let op = Cube.opNames[index];
    c.takeOperation(op);
    c.takeOperation(Cube.reverseOp(op));
    if (!c.isReset()) {
        throw ("Not reset after reverse!");
    }
}

console.log('\nShuffle 100 times:');
c.shuffle(100);
console.log('valid:', c.isValid());

console.log('\nRecover:');
c.recover();
console.log('Recovered: ', c.isReset());
