class IpHandle_IpAddr {

    constructor(ip, mask) {
        if (this.validateIp(ip)) {
            this._ip = ip;
        } else {
            console.log(ip);
            console.log(mask);
            throw "VALIDATION FAILURE - IP address is invalid.";
        }
        if (this.validateMask(mask)) {
            this._mask = mask;
        } else {
            console.log(ip);
            console.log(mask);
            throw "VALIDATION FAILURE - Mask is invalid.";
        }
        var networkAndBroadcast = this.evaluateAddresses();
        this._network = networkAndBroadcast[0];
        this._broadcast = networkAndBroadcast[1];
    }

    get ip() {
        return this._ip;
    }

    set ip(ip) {
        if (this.validateIp(ip)) {
            this._ip = ip;
        }
    }

    get mask() {
        return this._mask;
    }

    set mask(mask) {
        if (this.validateMask(mask)) {
            this._mask = mask;
        }
    }

    get network() {
        return this._network;
    }

    set network(network) {
        throw "SET FAILURE - Network address cannot be set manually."
    }

    get networkMagnitude() {
        return this._networkMagnitude;
    }

    set networkMagnitude(networkMagnitude) {
        throw "SET FAILURE - Network magnitude cannot be set manually."
    }

    get broadcast() {
        return this._broadcast;
    }

    set broadcast(broadcast) {
        throw "SET FAILURE - Broadcast address cannot be set manually."
    }

    get broadcastMagnitude() {
        return this._broadcastMagnitude;
    }

    set broadcastMagnitude(broadcastMagnitude) {
        throw "SET FAILURE - Broadcast magnitude cannot be set manually."
    }

    validateIp(ip) {
        var ipPattern = /(\d+[.]\d+[.]\d+[.]\d+)/i;
        var match = ipPattern.exec(ip);
        if (match) {
            var ipAddress = match[0];
            var ipSplit = ipAddress.split('.');
            if (ipSplit.length != 4) {
                throw "VALIDATION FAILURE - Invalid IP address - IP address must have four octets.";
            }
            for (var i = 0; i < ipSplit.length; ++i) {
                if (Number(ipSplit[i]) < 0 || Number(ipSplit[i]) > 255) {
                    throw "VALIDATION FAILURE - All octets must be between 0 and 255.";
                }
            }
            return true;
        } else {
            return false;
        }
    }

    validateMask(mask) {
        if (mask >= 0 && mask <= 32) {
            return true;
        } else {
            return false;
        }
    }

    validateMask_regex(mask) {
        var maskPattern = /\d+[.]\d+[.]\d+[.]\d+[/](\d+)/i;
        var match = maskPattern.exec(mask)
        if (match) {
            if (Number(mask) >= 0 && Number(mask) <= 32) {
                return true;
            } else {
                throw "VALIDATION FAILURE - Subnet mask must be a number between 0 and 32.";
            }
        } else {
            return false;
        }
    }

    evaluateAddresses() {
        if (this._ip && this._mask) {

            // network binary changes all mutable bits to 0; broadcast changes them to 1

            var ipSplit = this._ip.split('.');
            var binaryString = '';
            for (var i = 0; i < ipSplit.length; ++i) {
                var ipBinary = Number(ipSplit[i]).toString(2);
                var ipBinaryEightBit = ('00000000' + ipBinary).slice(-8);
                binaryString += ipBinaryEightBit;
            }
            var maskAmount = (32 - Number(this._mask));
            var newZeroes = '0'.repeat(maskAmount);
            var newOnes = '1'.repeat(maskAmount);
            var finalBinary_network = binaryString.substr(0, Number(this._mask)) + newZeroes;
            this._networkMagnitude = parseInt(finalBinary_network, 2);
            var finalBinary_broadcast = binaryString.substr(0, Number(this._mask)) + newOnes;
            this._broadcastMagnitude = parseInt(finalBinary_broadcast, 2);
            var networkIp = this.binaryToIp(finalBinary_network);
            var broadcastIp = this.binaryToIp(finalBinary_broadcast);
            return [networkIp, broadcastIp];
        } else {
            throw "Either IP address or subnet mask is invalid.";
        }
    }

    binaryToIp(binaryString) {
        var extraZeroesNeeded = binaryString.length % 8;
        if (extraZeroesNeeded > 0) {
            extraZeroesNeeded = 8 - extraZeroesNeeded;
            for (var i = 0; i < extraZeroesNeeded; ++i) {
                binaryString = '0' + binaryString;
            }
        }
        var octetPattern = /\d{8}/g;
        var octets = binaryString.match(octetPattern);
        if (octets.length != 4) {
            throw "Invalid binary string.";
        }
        for (var i = 0; i < octets.length; ++i) {
            octets[i] = parseInt(octets[i], 2);
        }
        var finalIp = octets.join('.');
        return finalIp;
    }

    getCidr() {
        return this._ip + '/' + this._mask;
    }

    debug_GetNetworkData() {
        return 'network address: ' + this._network + ', base 10 magnitude: ' + this._networkMagnitude;
    }

    debug_GetBroadcastData() {
        return 'broadcast address: ' + this._broadcast + ', base 10 magnitude: ' + this._broadcastMagnitude;
    }

}

function checkIpInclusion(firstIp, secondIp, checkLean) {
    if (firstIp instanceof IpHandle_IpAddr && secondIp instanceof IpHandle_IpAddr) {
        // very elementary check just to see if they are identical
        if (firstIp.ip === secondIp.ip && firstIp.mask === secondIp.mask) {
            return true;
        }
        var first_min = firstIp.networkMagnitude;
        var first_max = firstIp.broadcastMagnitude;
        var second_min = secondIp.networkMagnitude;
        var second_max = secondIp.broadcastMagnitude;
        if (checkLean) {
            return checkLeanInclusion(first_min, first_max, second_min, second_max);
        } else {
            var firstArray = [];
            for (var i = first_min; i <= first_max; ++i) {
                firstArray.push(i);
            }
            var secondArray = [];
            for (var i = second_min; i <= second_max; ++i) {
                secondArray.push(i);
            }
            var intersect = secondArray.filter(function(ipAddr) {
                return firstArray.indexOf(ipAddr) > -1;
            });
            if (intersect.length) {
                return true;
            } else {
                return false;
            }
        }
    } else {
        throw "This function works with two instances of the IpHandle_IpAddr class.";
    }
}

function debug_CheckIpInclusion(firstIp, secondIp) {
    var debugOutput = {'result': ''}
    if (firstIp instanceof IpHandle_IpAddr && secondIp instanceof IpHandle_IpAddr) {
        // very elementary check just to see if they are identical
        if (firstIp.ip === secondIp.ip && firstIp.mask === secondIp.mask) {
            debugOutput['result'] = 'Exact Match';
            return debugOutput;
        }
        var first_min = firstIp.networkMagnitude;
        debugOutput['first_min'] = first_min;
        var first_max = firstIp.broadcastMagnitude;
        debugOutput['first_max'] = first_max;
        var second_min = secondIp.networkMagnitude;
        debugOutput['second_min'] = second_min;
        var second_max = secondIp.broadcastMagnitude;
        debugOutput['second_max'] = second_max;
        var firstArray = [];
        for (var i = first_min; i <= first_max; ++i) {
            firstArray.push(i);
        }
        var secondArray = [];
        for (var i = second_min; i <= second_max; ++i) {
            secondArray.push(i);
        }
        var intersect = secondArray.filter(function(ipAddr) {
            return firstArray.indexOf(ipAddr) > -1;
        });
        if (intersect.length) {
            debugOutput['result'] = 'Ranges intersect';
        } else {
            debugOutput['result'] = 'Ranges do not intersect';
        }
        debugOutput['intersect'] = intersect;
        return debugOutput;
    } else {
        debugOutput['result'] = 'This function works with two instances of the IpHandle_IpAddr class.';
        return debugOutput;
    }
}

function checkIpEquality(firstIp, secondIp) {
    if (firstIp instanceof IpHandle_IpAddr && secondIp instanceof IpHandle_IpAddr) {
        // very elementary check just to see if they are identical
        if (firstIp.ip === secondIp.ip && firstIp.mask === secondIp.mask) {
            return true;
        } else {
            return false;
        }
    } else {
        throw "This function works with two instances of the IpHandle_IpAddr class.";
    }
}

function external_ValidateIp(ip) {
    var ipPattern = /(\d+[.]\d+[.]\d+[.]\d+)/i;
    var match = ipPattern.exec(ip);
    if (match) {
        var ipAddress = match[0];
        var ipSplit = ipAddress.split('.');
        if (ipSplit.length != 4) {
            return false;
        }
        for (var i = 0; i < ipSplit.length; ++i) {
            if (Number(ipSplit[i]) < 0 || Number(ipSplit[i]) > 255) {
                return false;
            }
        }
        return true;
    } else {
        return false;
    }
}

function external_BinaryToIp(binaryString) {
    var extraZeroesNeeded = binaryString.length % 8;
    if (extraZeroesNeeded > 0) {
        extraZeroesNeeded = 8 - extraZeroesNeeded;
        for (var i = 0; i < extraZeroesNeeded; ++i) {
            binaryString = '0' + binaryString;
        }
    }
    var octetPattern = /\d{8}/g;
    var octets = binaryString.match(octetPattern);
    if (octets.length != 4) {
        console.log(octets);
        throw "Invalid binary string.";
    }
    for (var i = 0; i < octets.length; ++i) {
        octets[i] = parseInt(octets[i], 2);
    }
    var finalIp = octets.join('.');
    return finalIp;
}

function external_MaskToCidr(subnetMask) {
    var subnetSplit = subnetMask.split('.');
    var maskTotal = 0;
    for (var i = 0; i < subnetSplit.length; ++i) {
        subnetSplit[i] = (+subnetSplit[i]).toString(2);
        maskTotal += subnetSplit[i].split('1').length - 1;
    }
    return maskTotal;
}

function debug_testLeanInclusion(firstIp, secondIp) {
    var first_min = firstIp.networkMagnitude;
    var first_max = firstIp.broadcastMagnitude;
    var second_min = secondIp.networkMagnitude;
    var second_max = secondIp.broadcastMagnitude;
    return checkLeanInclusion(first_min, first_max, second_min, second_max);
}

function checkLeanInclusion(first_min, first_max, second_min, second_max) {
    var conditionCheck = ( (first_min >= second_min && first_min <= second_max) || (first_max >= second_min && first_max <= second_max) );
    if (conditionCheck) {return true};
    var conditionCheck = ( (second_min >= first_min && second_min <= first_max) || (second_max >= first_min && second_max <= first_max) );
    return conditionCheck;
}
