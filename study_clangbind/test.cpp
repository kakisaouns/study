struct X{
    int value;

    void
    func(){}
};

int
plus(int a, int b){
    return a + b;
}

namespace hoge{
    int
    minus(int a, int b){
        return a - b;
    }
}

int
main(){
    plus(1, 2);
    hoge::minus(3, 5);
    return 0;
}